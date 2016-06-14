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

