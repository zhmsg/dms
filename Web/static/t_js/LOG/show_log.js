/**
 * Created by msg on 10/29/15.
 */
// $('#search_table').bind('input propertychange', function() {alert("success")});


function update_search_url(){
    var request_args = "?";
    var log_level = $("#log_level").val();
    var url_prefix = $("#url_prefix").val();
    request_args += "log_level=" + log_level + "&";
    request_args += "url_prefix=" + url_prefix + "&";
    $("#start_search").attr("href", request_args);

}
update_search_url();
