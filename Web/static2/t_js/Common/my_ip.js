/**
 * Created by msg on 6/14/16.
 */


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

var ip_info;

function get_ip_info_success(data){
    if(data.status == true){
        ip_info = data.data;
    }
    else{
        ip_info = null;
    }
}

function get_ip_info(ip_value){
    var local_ip = localStorage.getItem(ip_value);
    if(local_ip != null){
        console.info("from local get " + local_ip);
        return JSON.parse(local_ip);
    }
    var request_url = "/tools/ip/" + ip_value + "/";
    my_request(request_url, "GET", null, get_ip_info_success);
    localStorage.setItem(ip_value, JSON.stringify(ip_info));
    return ip_info;
}