from flask import Flask, request, send_from_directory, Response, render_template, redirect, g
import json
from threading import Thread
import serial
import requests
import webbrowser
import os
from time import sleep

ser = serial.Serial('/dev/cu.usbserial-A6026SIM', 9600)

BAUD_RATE = 9600
RFID_BYTES = 12
START_CHAR = '\x02'

TAGS_SEEN = []
global LOGGED_USER
LOGGED_USER = ""


def rfid_thread():
    while True:
        print ('Wating for RFID Tag......')
        # Wait until a tag is read
        rfid = ser.read(RFID_BYTES)
        rfid = str(rfid.strip(START_CHAR))
    
        # Only act if we think we have a valid tag
        if len(rfid) == (RFID_BYTES - 1):
            print 'Tag Found', rfid
            with open('data.json', 'r') as fp:
                data = json.load(fp)
                #New User - register
            if not rfid in data['registered_users']:
                data['registering'] = rfid
                with open('data.json', 'w') as fp:
                    json.dump(data, fp)
                webbrowser.open('http://localhost:8080/register', new=2)
            else:
                #Registered user
                data['logged_user']=rfid
                with open('data.json', 'w') as fp:
                    json.dump(data, fp)
                webbrowser.open('http://localhost:8080/pico', new=2)

    
            # Flush the bus
            ser.flushInput()

def cloud_poller_thread():
    while True:
        print ('Checking for Messages')
        #Get new messages
        r = requests.get('CLOUD_MSGS_ENDPOINT')
        in_msgs = r.json()
        if in_msgs:
            with open('data.json') as fp:
                data = json.load(fp)
            data['received_messages'] = in_msgs
            with open('data.json', 'w') as fp:
                json.dump(data, fp)
        sleep(5)
        
        

thread = Thread(target = rfid_thread)
thread.setDaemon(True)
thread.start()
#thread = Thread(target = cloud_poller_thread)
#thread.setDaemon(True)
#thread.start()

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')


msgs = [{"from":"kate andersen", "to":"Jenny", "date":"a date", "msg":"Here is some message content1"},
        {"from":"kate andersen", "to":"Jenny", "date":"a date", "msg":"Here is some message content2"},
        {"from":"kate andersen", "to":"Jenny", "date":"a date", "msg":"Here is some message content3"},
        {"from":"kate andersen", "to":"Jenny", "date":"a date", "msg":"Here is some message content4"}]


users = []


# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/logout')
def logout():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    data['logged_user'] = ''
    with open('data.json', 'w') as fp:
        json.dump(data, fp)
    return redirect("/pico", code=302)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        with open('data.json', 'r') as fp:
            data = json.load(fp)
        new_user = json.loads(request.get_json())
        new_user_id = data['registering']
        data['registered_users_data'][new_user_id]=new_user
        data['registered_users'].append(new_user_id)
        data.pop('registering')
        with open('data.json', 'w') as fp:
            json.dump(data, fp)
        return redirect("/pico?user={}".format(new_user_id), code=302)
    else:
        return send_from_directory("content", 'register.html')

@app.route('/pico')
def pico():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    if data['logged_user'] == '':
        #No one logged in - generic page
        return send_from_directory('content', 'generic.html')
    else:
        return send_from_directory('content', 'index.html')
    
@app.route('/qa')
def qa():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    if data['logged_user'] == '':
        #No one logged in - generic page
        return send_from_directory('content', 'generic.html')
    else:
        return send_from_directory('content', 'qa.html')

@app.route('/body_view')
def body_view():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    if data['logged_user'] == '':
        #No one logged in - generic page
        return send_from_directory('content', 'generic.html')
    else:
        return send_from_directory('content', 'body_view.html')
    

@app.route('/text_view')
def text_view():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    if data['logged_user'] == '':
        #No one logged in - generic page
        return send_from_directory('content', 'generic.html')
    else:
        return send_from_directory('content', 'text_view.html')
    
@app.route('/chat')
def chat():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    if data['logged_user'] == '':
        #No one logged in - generic page
        return send_from_directory('content', 'generic.html')    
    else:
        return send_from_directory('content', 'chat.html')
    

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('content/assets', path)

@app.route('/scripts/<path:path>')
def send_scripts(path):
    return send_from_directory('content/scripts', path)

@app.route('/logged_user')
def get_logged_user():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    return Response(json.dumps(data['registered_users_data'][data['logged_user']]))
        

@app.route('/local_msgs_received')
def get_local_msgs():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    return Response(json.dumps(data['received_messages']))


@app.route('/local_msgs_sending', methods=['POST'])
def local_msgs_sending():
    #Get some data and send to ro
    with open('data.json') as fp:
        data = json.load(fp)
    msgs = data['pending_messages']
    r = requests.post('https://roksonne.com/api/messages', 
                      data = {'rfid_tag':msgs[0]['tag'], 'body':msgs[0]['body']})
    return Response(r.json())



@app.route('/local_helpalert')
def local_helpalert():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    data['requested_help'] = data['logged_user']
    with open('data.json', 'w') as fp:
        json.dump(data, fp)
    #Send to Ro
    

@app.route('/local_reportabuse')
def local_reportabuse():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    data['reported_abuse'] = data['logged_user']
    with open('data.json', 'w') as fp:
        json.dump(data, fp)
    #Send to Ro

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
    
    
    
    
    