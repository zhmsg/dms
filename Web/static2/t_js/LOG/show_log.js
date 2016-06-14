/**
 * Created by msg on 10/29/15.
 */
// $('#search_table').bind('input propertychange', function() {alert("success")});

function format_time(t){
    t = t.replace(/([^\d:]*)/g, "");
    var ts = t.split(":");
    var ts_len = ts.length;
    if(ts_len != 3){
        return t;
    }
    var hour_s = ts[0];
    var minute_s = ts[1];
    var second_s = ts[2];
    if(hour_s == "" || minute_s == "" || second_s == ""){
        return t;
    }
    var hour = parseInt(hour_s);
    var minute = parseInt(minute_s);
    var second = parseInt(second_s);
    if(hour < 10){
        hour_s = "0" + hour;
    }
    else if(hour <= 23){
        hour_s = "" + hour;
    }
    else{
        hour_s = "00";
    }
    if(minute < 10){
        minute_s = "0" + minute;
    }
    else if(minute <= 59){
        minute_s = "" + minute;
    }
    else{
        minute_s = "00";
    }

    if(second < 10){
        second_s = "0" + second;
    }
    else if(second <= 59){
        second_s = "" + second;
    }
    else{
        second_s = "59";
    }
    t = hour_s + ":" + minute_s + ":" + second_s;
    return t;
}


function calc_time(t){
    t = t.replace(/([^\d:]*)/g, "");
    var ts = t.split(":");
    var ts_len = ts.length;
    if(ts_len != 3){
        return 0;
    }
    var now_time = new Date();
    var year = now_time.getFullYear();
    var month = now_time.getMonth() + 1;
    var day = now_time.getDate();
    var time_s = year + "/" + month + "/" + day + " " + t;
    try{
        return new Date(time_s).getTime() / 1000;
    }
    catch (e){
        return 0;
    }
    return 0;
}

function update_search_url(refresh){
    var request_args = "?";
    var start_time = calc_time($("#start_time").val());
    var end_time = calc_time($("#end_time").val());
    if(start_time > end_time && end_time > 0){
        start_time = start_time - 86400;
    }
    var log_level = $("#log_level").val();
    var url_prefix = $("#url_prefix").val();
    var show_before = $("#show_before").val();
    var account = $("#account").val();
    if(log_level == "all") {
        if ($("#show_before").is(':checked')) {
            request_args += "look_before=1&"
        }
        $("#lab_show_before").show();
    }
    else{
        $("#lab_show_before").hide();
    }
    request_args += "start_time=" + start_time + "&";
    request_args += "end_time=" + end_time + "&";
    request_args += "log_level=" + log_level + "&";
    request_args += "url_prefix=" + url_prefix + "&";
    request_args += "account=" + account;
    $("#start_search").attr("href", request_args);
    if(refresh == 1){
        location.href = request_args;
    }

}

$(function(){
    $("input[id$=_time]").blur(function(){
        var v = this.value;
        this.value = format_time(v);
        update_search_url(0);
    });
    $("td[name='run_begin']").click(function(){
        var click_text = format_time(this.innerText);
        var start_text = $("#start_time").val();
        var end_text = $("#end_time").val();
        var click_time = calc_time(click_text);
        if(click_time == 0){
            return;
        }
        var start_time = calc_time(start_text);
        var end_time = calc_time(end_text);
        if(click_time > end_time){
            $("#end_time").val(click_text);
        }
        else if(start_time > click_time || start_time == 0){
            $("#start_time").val(click_text);
        }
        //else{
        //    $("#end_time").val(click_text);
        //}
        update_search_url(0);
    });
    var request_ips = $("td[name='request_ip']");
    for(var i=0;i<request_ips.length;i++){
        var td_ip = request_ips[i];
        var ip_value = td_ip.innerHTML;
        td_ip.innerHTML = ip_2_str(ip_value);
        var local_ip = localStorage.getItem(ip_value);
        var ip_info = null;
        if(local_ip != null){
            console.info("from local get " + local_ip);
            ip_info = JSON.parse(local_ip);
        }
        else {
            ip_info = get_ip_info(ip_value);
            td_ip.className = "redBg";
        }
        if(ip_info != null){
            td_ip.title = ip_info["info1"];
        }
    }
    $("td[name='request_account']").click(function(){
        $("#account").val(this.innerText);
        update_search_url(0);
    });
    $("td[name='request_url']").click(function(){
        $("#url_prefix").val(this.innerText);
        update_search_url(0);
    });
    update_search_url(0);
});