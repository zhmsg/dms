/**
 * Created by msg on 02/07/17.
 */
//

$(function(){
    var request_ips = $("td[name$='_ip']");
    for(var i=0;i<request_ips.length;i++){
        var td_ip = request_ips[i];
        var j_td_ip = $(td_ip);
        var ip_value = j_td_ip.text();
        j_td_ip.text(ip_2_str(ip_value));
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
        var td_name = j_td_ip.attr("name");
        if(td_name == "user_ip"){
            $(td_ip).next().text(j_td_ip.attr("title"));
        }
    }

    var login_timestamps = $("td[name='login_time']");
    for(var i=0;i<login_timestamps.length;i++){
        var td_time = $(login_timestamps[i]);
        var time_stamp = td_time.text();
        td_time.text(timestamp_2_datetime(time_stamp));
    }
});