/**
 * Created by msg on 11/15/16.
 */

function init_token(){
    var token_url = "https://gene.ac/wx/token/";
    my_async_request(token_url, "GET", null, init_ticket)
}

function init_ticket(data){
    if(data.status % 1000 !=  1){
        console.info(data);
        return false;
    }
    var access_token = data.data;
    console.info(access_token);
    var ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=" + access_token + "&type=jsapi";
    my_async_request(ticket_url, "GET", null, init_wx);
}

function init_wx(data){
    if(data.errcode != 0){
        console.info(data);
        return false;
    }
    var ticket = data.ticket;
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
    init_token();
   alert("success");
});