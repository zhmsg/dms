/**
 * Created by msg on 6/17/16.
 */


function check_input_ip(el){
    var ip_str = el.value;
    var ip_value = ip_str.search(/[^\d]+/i);
    if(ip_value != -1){
        console.info("now input ip str");
        ip_str = format_ip(ip_str);
        $("#ip_str").text(ip_str);
        ip_value = str_2_ip(ip_str);
    }
    else{
        ip_value = parseInt(ip_str);
    }
    if(ip_value >= 0) {
        $("#btn_q_ip").removeAttr("disabled");
        console.info(ip_value);
    }
    else{
        $("#btn_q_ip").attr("disabled", "disabled");
    }
}

$(function(){
    $("#btn_q_ip").click(function(){
        var ip_str = $("#input_ip").val();
        var ip_value = ip_str.search(/[^\d]+/i);
        if(ip_value != -1){
            console.info("now input ip str");
            ip_str = format_ip(ip_str);
            $("#ip_str").text(ip_str);
            ip_value = str_2_ip(ip_str);
        }
        else{
            ip_value = parseInt(ip_str);
        }
        if(ip_value >= 0) {
            $("#btn_q_ip").removeAttr("disabled");
            var local_ip = localStorage.getItem(ip_value);
            var ip_info = null;
            if(local_ip != null){
                console.info("from local get " + local_ip);
                ip_info = JSON.parse(local_ip);
            }
            else {
                ip_info = get_ip_info(ip_value);
            }
            if(ip_info != null){
                $("#ip_value").text(ip_value);
                $("#ip_info1").text(ip_info["info1"]);
                $("#ip_info2").text(ip_info["info2"]);
            }
        }
        else{
            $("#ip_str").text("");
            $("#ip_value").text("");
            $("#ip_info1").text("");
            $("#ip_info2").text("");
        }
    });

});