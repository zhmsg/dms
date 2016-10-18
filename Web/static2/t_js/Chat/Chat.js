/**
 * Created by msg on 10/12/16.
 */
var ws_service = "ws://" + location.host + "/chat/msg/";

function Init_WebSocket(ws_service){
    ws = new WebSocket(ws_service);
    ws.onmessage = function(event) {
        var table = document.getElementById('chat_message');
        var msg = JSON.parse(event.data);
        var insert_row = table.insertRow();
        insert_row.insertCell().innerHTML = msg["sender"];
        insert_row.insertCell().innerHTML = msg["msg"];
    };
    ws.onopen = function(event) {
        var current_user_name = $("#current_user_name").val();
        var login_msg = JSON.stringify({"msg_type": "login", "data": current_user_name});
        ws.send(login_msg);
    };
    ws.onclose = function(event) {
        var table = document.getElementById('chat_message');
        var insert_row = table.insertRow();
        insert_row.insertCell().innerHTML = "local";
        insert_row.insertCell().innerHTML = "连接已断开";
        ws = Init_WebSocket(ws_service);
    };
    ws.onerror = function(event) {

        //ws = new WebSocket('ws://' + ws_service + '/chat/msg/');
    };
    return ws;
}

var ws = Init_WebSocket(ws_service);
function send() {
    var msg_info = JSON.stringify({"msg_type": "msg", "data": document.getElementById('chat').value});
    ws.send(msg_info);
    document.getElementById('chat').value = '';
}