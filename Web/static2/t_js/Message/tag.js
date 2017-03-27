/**
 * Created by msg on 2/9/17.
 */

function handler_tags(tags_data) {
    var data_len = tags_data.length;
    var t_name = "t_tag";
    clear_table(t_name);
    if (data_len == 0) {
        add_row_td(t_name, "暂无标签");
    }
    for (var i = 0; i < data_len; i++) {
        var data_item = tags_data[i];
        var add_tr = $("<tr></tr>");
        add_tr.append(new_td("message_tag", data_item));
        var email_td = $("<td>不通知</td>");
        if ((data_item["notify_mode"] & 1) == 1) {
            email_td.text("通知");
        }
        add_tr.append(email_td);
        var wx_td = $("<td>不通知</td>");
        if ((data_item["notify_mode"] & 2) == 2) {
            wx_td.text("通知");
        }
        add_tr.append(wx_td);
        var ding_td = $("<td>不通知</td>");
        if ((data_item["notify_mode"] & 4) == 4) {
            ding_td.text("通知");
        }
        add_tr.append(ding_td);
        add_tr.append(new_td("interval_time", data_item));
        var time_td = $("<td></td>");
        time_td.text(timestamp_2_datetime(data_item["insert_time"]));
        add_tr.append(time_td);
        $("#" + t_name).append(add_tr);
    }

}

$(document).ready(function () {
    var tag_url = $("#tag_url").val();
    my_async_request2(tag_url, "GET", null, handler_tags);
});