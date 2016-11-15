/**
 * Created by msg on 11/15/16.
 */

function init_ticket_signature(){
    var ticket_url = "http://wx.gene.ac/wx/ticket/signature/";
    var request_data = {"ref_url": location.href};
    my_async_request(ticket_url, "POST", request_data, init_wx)
}

function pay(){
    wx.startRecord();
}

function init_wx(data){
    if(data.status % 1000 !=  1){
        console.info(data);
        return false;
    }
    var sign_info = data.data;
    console.info(sign_info);
    wx.config({
        debug:true,
        appId:sign_info.app_id,
        timestamp: sign_info.timestamp,
        nonceStr: sign_info.nonceStr,
        signature: sign_info.signature,
        jsApiList:['startRecord', 'getNetworkType', 'chooseWXPay']
    });
    wx.ready(function(){
        alert("success");
    });
    wx.error(function(res){
       alert(res);
    });
}

$(function(){
    init_ticket_signature();
});