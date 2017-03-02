/**
 * Created by msg on 2/7/17.
 */

function timestamp_2_datetime(ts){
    var dt = new Date(parseInt(ts) * 1000);
    var dt_str = dt.toLocaleDateString().replace(/\//g, "-") + " ";
    dt_str += dt.toTimeString().substr(0, 8);
    return dt_str;
}

function get_timestamp(){
    return (new Date()).valueOf();
}


function get_timestamp2(){
    return parseInt(get_timestamp() / 1000);
}


function datetime_2_timestamp(dt_str){
    var ts = Date.parse(dt_str);
    return ts / 1000;
}

function today_timestamp(){
    var today = new Date();
    return datetime_2_timestamp(today.toLocaleDateString());
}

function duration_show(d){
    var s_duration = ""; //"(" + d + "秒)";
    var r = d % 60;
    s_duration = r + "秒" + s_duration;
    d = parseInt(d / 60);
    if(d <= 0){
        return s_duration;
    }
    r = d % 60;
    s_duration = r + "分" + s_duration;
    d = parseInt(d / 60);
    if(d <= 0){
        return s_duration;
    }
    r = d % 60;
    s_duration = r + "小时" + s_duration;
    d = parseInt(d / 60);
    if(d <= 0){
        return s_duration;
    }
    s_duration = d + "天" + s_duration;

    return s_duration;
}