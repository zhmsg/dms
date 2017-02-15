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

function datetime_2_timestamp(dt_str){
    var ts = Date.parse(dt_str);
    return ts / 1000;
}