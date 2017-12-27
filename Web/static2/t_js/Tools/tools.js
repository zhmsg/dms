/**
 * Created by msg on 6/17/16.
 */

var ss_groups = "ss_dms_ip_groups";

function check_input_ip(el){
    var ip_str = el.value;
    var ip_value = ip_str.search(/[^\d]+/i);
    if(ip_value != -1 || ip_str.length <= 0){
        console.info("now input ip str");
        ip_str = format_ip(ip_str);
        $("#ip_str").text(ip_str);
        ip_value = str_2_ip(ip_str);
    }
    else{
        ip_value = parseInt(ip_str);
        $("#ip_str").text(ip_2_str(ip_value));
    }
    if(ip_value >= 0) {

        $("#ip_value").text(ip_value);
        $("#btn_q_ip").removeAttr("disabled");
        console.info(ip_value);
    }
    else{
        $("#ip_value").text("");
        $("#btn_q_ip").attr("disabled", "disabled");
    }
    $("#ip_info1").text("");
    $("#ip_info2").text("");
    $("#ip_group").text("");
}

function receive_group_data(data){
    sessionStorage.setItem(ss_groups, JSON.stringify(data));
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
        else {
            ip_value = parseInt(ip_str);
        }
        if(ip_value >= 0) {
            $("#btn_q_ip").removeAttr("disabled");
            $("#ip_str").text(ip_2_str(ip_value));
            $("#ip_value").text(ip_value);
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
                $("#ip_info1").text(ip_info["info1"]);
                $("#ip_info2").text(ip_info["info2"]);
            }
            var g_data_s = sessionStorage.getItem(ss_groups);
            var ip_groups = "";
            if(g_data_s != null){
                var g_data = JSON.parse(g_data_s);
                for(var i=0;i<g_data.length;i++){
                    var g_item = g_data[i];
                    if(ip_value <= g_item["ip_e"] && ip_value >= g_item["ip_s"]){
                        ip_groups += g_item["g_name"] + " ";
                        console.info(g_item);
                    }
                }
            }
            $("#ip_group").text(ip_groups);
        }
        else{
            $("#ip_str").text("");
            $("#ip_value").text("");
            $("#ip_info1").text("");
            $("#ip_info2").text("");
            $("#ip_group").text("");
        }
    });
    $("#btn_q_ip").click();
    var ip_group_url = $("#ip_group_url").val();
    my_async_request2(ip_group_url, "GET", null, receive_group_data);
});