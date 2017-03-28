/**
 * Created by msg on 2/9/17.
 */

var request_tag_flag = new Object();

function handler_tags(tags_data) {
    var data_len = tags_data.length;
    var t_name = "t_tag";
    clear_table(t_name);
    if (data_len == 0) {
        add_row_td(t_name, "暂无标签");
    }
    var lab_text = '<label class="checkbox-inline"><input type="checkbox" class="left5" />通知</label>';
    for (var i = 0; i < data_len; i++) {
        var data_item = tags_data[i];
        var add_tr = $("<tr></tr>");

        add_tr.append(new_td("message_tag", data_item));

        var email_td = $('<td></td>');
        email_td.append($(lab_text));
        if ((data_item["notify_mode"] & 1) == 1) {
            email_td.find("input").attr("checked", "checked");
        }
        email_td.attr("name", "td_notify_email");
        add_tr.append(email_td);

        var wx_td = $('<td></td>');
        wx_td.append($(lab_text));
        if ((data_item["notify_mode"] & 2) == 2) {
            wx_td.find("input").attr("checked", "checked");
        }
        wx_td.attr("name", "td_notify_wx");
        add_tr.append(wx_td);

        var ding_td = $('<td></td>');
        ding_td.append($(lab_text));
        if ((data_item["notify_mode"] & 4) == 4) {
            ding_td.find("input").attr("checked", "checked");
        }
        ding_td.attr("name", "td_notify_ding");
        add_tr.append(ding_td);

        add_tr.append(new_td("interval_time", data_item, null, true));

        var time_td = $("<td></td>");
        time_td.text(timestamp_2_datetime(data_item["insert_time"]));
        add_tr.append(time_td);

        add_tr.append(new_td("user_name", data_item));

        if (data_item["user_name"] == $("#current_user_name").val()) {
            var op_td = $("<td></td>");
            op_td.append("<a>删除</a>");
            add_tr.append(op_td);

            add_tr.attr("message_tag", data_item["message_tag"]);
            add_tr.attr("notify_mode", data_item["notify_mode"]);
            add_tr.attr("interval_time", data_item["interval_time"]);

            add_tr.find("label").children().click(function () {
                var parent_tr = $(this).parents("tr");
                var message_tag = parent_tr.attr("message_tag");
                //  判断是否和已有的有变化
                var update_info = judge_tr_update(parent_tr);
                if (update_info != null) {
                    if (message_tag in request_tag_flag && request_tag_flag[message_tag] == true) {
                        console.info("wait ...");
                    }
                    else {
                        request_tag_flag[message_tag] = true;
                        window.setTimeout(function () {
                            start_update_tag(message_tag);
                        }, 1500);
                    }
                }
                else {
                    console.info("not need start");
                }
            });
            add_tr.find("td[name='td_interval_time'] input").change(function () {
                    var parent_tr = $(this).parents("tr");
                    var message_tag = parent_tr.attr("message_tag");
                    //  判断是否和已有的有变化
                    var update_info = judge_tr_update(parent_tr);
                    if (update_info != null) {
                        if (message_tag in request_tag_flag && request_tag_flag[message_tag] == true) {
                            console.info("wait ...");
                        }
                        else {
                            request_tag_flag[message_tag] = true;
                            window.setTimeout(function () {
                                start_update_tag(message_tag);
                            }, 1500);
                        }
                    }
                    else {
                        console.info("not need start");
                    }
                }
            )
            ;
        }
        else {
            var op_td = $("<td></td>");
            add_tr.append(op_td);
            add_tr.find("input").attr("disabled", "disabled");
        }

        $("#" + t_name).append(add_tr);
    }

}

function judge_include_value(base_value, v) {
    var r = base_value & v;
    if (r == v)
        return true;
    else
        return false;
}

function judge_tr_update(tr_el) {
    var notify_tds = {"td_notify_email": 1, "td_notify_wx": 2, "td_notify_ding": 4};
    var message_tag = tr_el.attr("message_tag");
    var update_info = {"message_tag": message_tag};
    var notify_mode = parseInt(tr_el.attr("notify_mode"));
    var interval_time = tr_el.attr("interval_time");
    var has_update = false;
    for (var key in notify_tds) {
        var current_stage = tr_el.find("td[name='" + key + "'] input").is(":checked");
        if (current_stage != judge_include_value(notify_mode, notify_tds[key])) {
            has_update = true;
            if (current_stage == true) {
                notify_mode += notify_tds[key];
            } else
                notify_mode -= notify_tds[key];
            update_info["notify_mode"] = notify_mode;
        }
    }
    var current_interval_time = tr_el.find("td[name='td_interval_time'] input").val();
    if (interval_time != current_interval_time) {
        has_update = true;
        update_info["interval_time"] = current_interval_time;
    }
    if (has_update == false) {
        return null;
    }
    else {
        return update_info
    }
}

function update_success(update_data) {
    if (update_data["exec_r"] == 1) {
        var current_tr = $("tr[message_tag='" + update_data["message_tag"] + "']");
        for (var key in update_data) {
            current_tr.attr(key, update_data[key]);
        }
    }
    else {
        console.info("not update");
    }
}

function start_update_tag(message_tag) {
    console.info("start update tag");
    var current_tr = $("tr[message_tag='" + message_tag + "']");
    var update_info = judge_tr_update(current_tr);
    if (update_info == null) {
        console.info("no update info");
    }
    else {
        var tag_url = $("#tag_url").val();
        my_async_request2(tag_url, "PUT", update_info, update_success);
        console.info(update_info);
    }
    if (message_tag in request_tag_flag) {
        request_tag_flag[message_tag] = false;
    }
}

function add_tag() {
    var message_tag = $("#message_tag").val();
    var interval_time = $("#interval_time").val();
    var notify_mode = 0;
    var r_data = {"message_tag": message_tag, "interval_time": interval_time};
    if ($("input[name='email_notify']").is(':checked')) {
        notify_mode += 1;
    }
    if ($("input[name='wx_notify']").is(':checked')) {
        notify_mode += 2;
    }
    if ($("input[name='ding_notify']").is(':checked')) {
        notify_mode += 4;
        var access_ding = $("#access_ding").val();
        r_data["access_ding"] = access_ding;
    }
    r_data["notify_mode"] = notify_mode;
    var tag_url = $("#tag_url").val();
    my_async_request2(tag_url, "POST", r_data);
}

function show_access_ding() {
    var current_lab = $(this);
    if (current_lab.find("input[name='ding_notify']").is(':checked')) {
        $("#li_access_ding").show();
    }
    else {
        $("#li_access_ding").hide();
    }
}

$(document).ready(function () {
    var tag_url = $("#tag_url").val();
    my_async_request2(tag_url, "GET", null, handler_tags);
    $("#btn_new_tag").click(add_tag);
    $("#lab_ding_notify").click(show_access_ding);
    $("#interval_time").keyup(function () {
        $("#interval_time").val(format_num($("#interval_time").val()));
    });
});