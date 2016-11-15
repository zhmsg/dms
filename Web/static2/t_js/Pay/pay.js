/**
 * Created by msg on 11/15/16.
 */

function init_ticket(){
    var ticket_url = "https://gene.ac/wx/ticket/";
    my_async_request(ticket_url, "GET", null, init_wx)
}


function init_wx(data){
    if(data.status % 1000 !=  1){
        console.info(data);
        return false;
    }
    var ticket = data.data;
    console.info(ticket);
    var timestamp = Date.parse(new Date()) / 1000;
    var nonceStr = "oiwefsdsrkljalwr23wrfs";
    console.info(timestamp);
    wx.config({
        debug:true,
        appId:"wx6b30be0bc9149832",
        timestamp: timestamp,
        nonceStr: nonceStr
    });
}

$(function(){
    init_ticket();
   alert("success");
});