/**
 * Created by msg on 9/23/16.
 */

function get_success(data){
    for(var i=0;i<data.data.length;i++){
        Add_TR(data.data[i]);
    }
}

$(function() {
    my_async_request(location.href, "GET", null, get_success);
});