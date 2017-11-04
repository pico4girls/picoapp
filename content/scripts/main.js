//Pico Pi Site

function sendTextData() {
    console.log("Send text data.")
    var endpoint = '/local_msgs_sending';
    $.ajax({ 
        type: "POST",
        url: endpoint,
        data: $('#myForm').serializeArray(),
        success: function () {
            alert('Posted question');
        }
    });
  }

  function reportAbuse() {
    console.log("reportAbuse")
    var endpoint = '/local_reportabuse';
    $.ajax({ 
        type: "POST",
        url: endpoint,
        data: "Reporting Abuse" + Date().toLocaleString(),
        success: function () {
            alert('Posted abuse alert');
        }
    });
  }

  function helpAlert() {
    console.log("helpAlert")
    var endpoint = '/local_helpalert';
    $.ajax({ 
        type: "POST",
        url: endpoint,
        data: "HELP ALERT" + + Date().toLocaleString(),
        success: function () {
            alert('Posted help alert');
        }
    });
  }

  //get messages from API
function getPeerMessages() {
    jQuery.ajax({
        url: "/local_peermsgs_received",
        type: "GET",
        contentType: 'application/json; charset=utf-8'
    }).done(function (data) {

        $.getJSON("example.json", function (json) {
            console.log(json);
            data = JSON.parse(json);
        });

        var $newsList = $('#AnswersList > ul');
        $.each(data, function (i, item) {
            $('<li>')
                .append($('<div>').html(item.date))
                .append($('<p>').html(item.value))
                .appendTo($newsList);
        });
    });
}

function getProfessionalMessages() {
    jQuery.ajax({
        url: "/local_msgs_received",
        type: "GET",
        contentType: 'application/json; charset=utf-8'
    }).done(function (data) {

        $.getJSON("example.json", function (json) {
            console.log(json);
            data = JSON.parse(json);
        });

        var $newsList = $('#AnswersList > ul');
        $.each(data, function (i, item) {
            $('<li>')
                .append($('<div>').html(item.date))
                .append($('<p>').html(item.value))
                .appendTo($newsList);
        });
    });
}