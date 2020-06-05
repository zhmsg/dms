/**
 * Created by msg on 11/15/16.
 */

function init_ticket_signature() {
    var ticket_url = "http://wx.gene.ac/wx/ticket/signature/";
    var request_data = {"ref_url": location.href};
    my_async_request(ticket_url, "POST", request_data, init_wx)
}

function pay() {
    my_async_request2(location.href, "POST", null, start_pay)
}

function pay_success(res) {
    console.info("成功返回");
    console.info(res);
    alert("success");
}

function start_pay(data) {
    //console.info(data);
    //alert("start pay");
    //var pay_info = data;
    //pay_info["success"] = pay_success;
    //wx.chooseWXPay(pay_info);
    function onBridgeReady() {
        WeixinJSBridge.invoke(
            'getBrandWCPayRequest', data,
            function (res) {
                alert(res.err_msg);
                if (res.err_msg == "get_brand_wcpay_request：ok") {
                }     // 使用以上方式判断前端返回,微信团队郑重提示：res.err_msg将在用户支付成功后返回    ok，但并不保证它绝对可靠。
                console.info(res);
                alert(res);
            }
        );
    }

    if (typeof WeixinJSBridge == "undefined") {
        if (document.addEventListener) {
            document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
        } else if (document.attachEvent) {
            document.attachEvent('WeixinJSBridgeReady', onBridgeReady);
            document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
        }
    } else {
        onBridgeReady();
    }
}

function init_wx(data) {
    if (data.status % 1000 != 1) {
        console.info(data);
        return false;
    }
    var sign_info = data.data;
    console.info(sign_info);
    wx.config({
        debug: true,
        appId: sign_info.app_id,
        timestamp: sign_info.timestamp,
        nonceStr: sign_info.nonceStr,
        signature: sign_info.signature,
        jsApiList: ['startRecord', 'getNetworkType', 'chooseWXPay']
    });
    wx.ready(function () {
        alert("success");
    });
    wx.error(function (res) {
        alert(res);
    });
}

$(function () {
    //init_ticket_signature();
});