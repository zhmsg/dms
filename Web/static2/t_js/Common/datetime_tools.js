/**
 * Created by msg on 2/7/17.
 */

function timestamp_2_datetime(ts){
    var dt = new Date(parseInt(ts) * 1000);
    var dt_str = dt.toLocaleDateString().replace(/\//g, "-") + " ";
    dt_str += dt.toTimeString().substr(0, 8);
    return dt_str;
}