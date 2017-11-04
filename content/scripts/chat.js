function getChats() {
var endpoint = '/local_msgs_sending';
/*$.ajax({ 
    type: "POST",
    url: endpoint,
    data: $('#myForm').serializeArray(),
    success: function () {
        alert('Posted question');
    }
}).done(function() {
	
});
*/
var html = '<div class="container"><row><column>';
    for (var i = 0; i <=5; i++) {
    		html+='<row>';
    		html+='<p>Some text here '+i+'</p>';
    		html+='</row>';
    		
    html += '</row></column></div>';
return html;
}