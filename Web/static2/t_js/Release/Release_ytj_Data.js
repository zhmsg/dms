/**
 * Created by msg on 9/7/16.
 */

function receive_success(data)
{
    if(data.status != 2){
        sweetAlert(data.message);
    }
    else{
        var secret_key = data.secret_key;
        release_ytj(secret_key);
    }
}

function receive_secret_key(){
    $("#btn_release_ytj").attr("disabled", "disabled");
    var request_url = "http://local.gene.ac:3285/yitiji/fabu/";
    my_async_request(request_url, "GET", null, receive_success);
}

function release_success(data)
{
    sweetAlert(data.message);
}

function release_ytj(secret_key)
{
    var service_ip = $("#service_IP").val();
    var release_style = $("#use_style").val();
    var request_data = "secret_key=" + secret_key +"&ip=" + service_ip + "&style=" + release_style;
    //var request_data = {"secret_key": secret_key, "ip": service_ip, "style": release_style};
    console.info(request_data);
    var request_url = "http://local.gene.ac:3285/yitiji/fabu/";
    my_async_form_request(request_url, "POST", request_data, release_success)
}

$(function(){
    $("#btn_release_ytj").click(receive_secret_key);
    $("#service_IP").keyup(function()
    {
        $("#service_IP").val(format_ip($("#service_IP").val()));
    });
});