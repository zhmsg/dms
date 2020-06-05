/**
 * Created by msg on 9/23/16.
 */

function get_success(data){
    $("#" + "t_params_info" + " tr").not(":first").remove();
    for (var i = 0; i < data.length; i++) {
        Add_TR(data[i]);
    }
}

$(function() {
    $("#btn_query").click(function () {
        var query_params = $("#query_params").val();
        if (query_params.length > 0) {
            my_async_request2(location.href + "query/?params=" + query_params, "GET", null, get_success);
        }
        else {
            my_async_request2(location.href, "GET", null, get_success);
        }
    });
    $("#btn_query").click();
});