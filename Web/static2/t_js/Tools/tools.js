/**
 * Created by msg on 6/17/16.
 */


function check_input_ip(el){
    var ip_str = el.value;
    var ip_value = parseInt(ip_str);
    if(ip_value == NaN){
        ip_str = format_ip(ip_str);
        el.value = ip_str;
        ip_value = str_2_ip(ip_str);
    }

    if(ip_value >= 0) {
        console.info(ip_value);
    }

}