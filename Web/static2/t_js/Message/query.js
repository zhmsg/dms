/**
 * Created by msg on 2/9/17.
 */

function show_message(message_data) {
    if (message_data.length > 0) {
        var message_item = message_data[0];
        var keys = ["message_tag", "message_id", "message_content"];
        for (var i in keys) {
            var key = keys[i];
            $("#div_show_message [name='" + key + "']").val(message_item[key]);
        }
        var pk = "publish_time";
        $("#div_show_message [name='" + pk + "']").val(timestamp_2_datetime(message_item[pk] / 1000));
    }
    else {
        var mk = "message_id";
        $("#div_show_message [name='" + mk + "']").val("未查询到");
    }
}

$(document).ready(function () {
    var args_keys = ["message_id", "topic_name", "topic_owner"];
    for (var i in args_keys) {
        var key = args_keys[i];
        var arg_v = UrlArgsValue(location.href, key);
        if (arg_v != null) {
            $("#query_" + key).val(arg_v);
        }
    }
    $("#btn_query_message").click(function () {
        var query_url = $("#query_url").val();
        var message_id = $("#query_message_id").val();
        if (message_id.length < 1) {
            return;
        }
        var topic_name = $("#query_topic_name").val();
        var topic_owner = $("#query_topic_owner").val();
        query_url += "?message_id=" + message_id;
        if (topic_name.length > 0) {
            query_url += "&topic_name=" + topic_name;
        }
        if (topic_owner.length > 0) {
            query_url += "&topic_owner=" + topic_owner;
        }
        my_async_request2(query_url, "GET", null, show_message);
    });
    if ($("#query_message_id").val().length > 1) {
        $("#btn_query_message").click();
        console.info($("#ul_menu li:eq(2)"));
        $("#ul_menu li:eq(2)").find("a").click();
    }
});