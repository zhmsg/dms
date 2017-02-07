/**
 * Created by msg on 6/14/16.
 */


function format_ip(ip_str) {
    ip_str = ip_str.replace(/([^\d.]*)/g, "");
    if(ip_str == ""){
        return ip_str;
    }
    var ts = ip_str.split(".");
    var ts_len = ts.length;
    if (ts_len > 4) {
        ts_len = 4;
    }
    ip_str = "";
    var ip_p = 0;
    for (var i = 0; i < ts_len; i++) {
        if(ts[i] == ""){
            if(i == ts_len - 1){
                ip_str += "."
            }
            continue;
        }
        ip_p = parseInt(ts[i]);
        if (ip_p > 255) {
            ip_p = 255;
        }
        ip_str += "." + ip_p;
    }
    return ip_str.substr(1);
}


function ip_2_str(ip_value){
    var ip_i = parseInt(ip_value);
    if(ip_i == NaN){
        return ip_value;
    }
    var ip_str = "";
    var i = 0;
    while(i < 4  || ip_i > 0)
    {
        ip_str = "." + ip_i % 256 + ip_str;
        ip_i = parseInt(ip_i / 256);
        i++;
    }
    return ip_str.substr(1);
}

function str_2_ip(ip_str){
    var ip_s = ip_str.split(".");
    if(ip_s.length != 4){
        return -1;
    }
    var base_num = new Array(16777216 ,65536 ,256, 1);
    var ip_value = 0;
    for(var i=0;i<4;i++){
        var p_i = parseInt(ip_s[i]);
        if(p_i == NaN){
            return -1;
        }
        if(p_i < 0 || p_i > 255){
            return -1;
        }
        ip_value += p_i * base_num[i];
    }
    return ip_value;
}

var ip_info;

function get_ip_info_success(data) {
    ip_info = data;
}

function get_ip_info(ip_value){
    var storage_prefix = "ip_info";
    var item_key = storage_prefix + ip_value;
    var local_ip = localStorage.getItem(item_key);
    if(local_ip != null && local_ip != "undefined"){
        console.info("from local get " + local_ip);
        return JSON.parse(local_ip);
    }
    var request_url = "/tools/ip/" + ip_value + "/";
    my_request2(request_url, "GET", null, get_ip_info_success);
    localStorage.setItem(item_key, JSON.stringify(ip_info));
    return ip_info;
}