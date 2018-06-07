/**
 * Created by msg on 2/9/17.
 */

var request_tag_flag = new Object();
var notify_tds = {"td_notify_email": 1, "td_notify_wx": 2, "td_notify_ding": 4};
var g_tags_vm = null;

function format_access_ding(el) {
    var current_access_ding = el.val();
    if (current_access_ding.indexOf("access_token=") >= 0) {
        current_access_ding = current_access_ding.substr(current_access_ding.indexOf("access_token=") + 13);
        el.val(current_access_ding);
    }
    return current_access_ding;
}

function prepare_update(parent_tr) {
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

function judge_include_value(base_value, v) {
    var r = base_value & v;
    if (r == v)
        return true;
    else
        return false;
}

function tag_info_2_tr(tag_info, current_tr) {
    for (var key in tag_info) {
        current_tr.attr(key, tag_info[key]);
    }
}

function show_msg(msg)
{
    $("div[role='alert']").hide();
    var dialog_div = $('<div class="alert alert-success" role="alert"></div>');
    $("body").append(dialog_div);
    register_reset_bottom(dialog_div);
    setTimeout(function () {
        dialog_div.remove();
    }, 2000);
    dialog_div.text(msg)
}
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

        for (var key in notify_tds) {
            var one_notify_td = $('<td></td>');
            one_notify_td.append($(lab_text));
            if (judge_include_value(data_item["notify_mode"], notify_tds[key])) {
                one_notify_td.find("input").attr("checked", "checked");
            }
            one_notify_td.attr("name", key);
            add_tr.append(one_notify_td);
        }

        add_tr.append(new_td("interval_time", data_item, null, true));

        var time_td = $("<td></td>");
        time_td.text(timestamp_2_datetime(data_item["insert_time"]));
        add_tr.append(time_td);

        add_tr.append(new_td("user_name", data_item));
        var op_td = $("<td name='td_op'></td>");
        add_tr.append(op_td);
        add_tr.find("input").attr("disabled", "disabled");

        tag_info_2_tr(data_item, add_tr);

        $("#" + t_name).append(add_tr);
        var row_td = add_row_td(t_name, "");
        row_td.attr("name", "tr_ding_setting");
        row_td.append('<label for="">钉钉Token：</label><input class="box-side width600 margin10" name="access_ding" type="text"/><label for="">钉的方式：</label><select class="box-side width300" name="ding_mode"><option value="1">文本方式</option><option value="2" selected>链接方式</option></select>');
        row_td.find("input[name='access_ding']").val(data_item["access_ding"]);
        row_td.find("select[name='ding_mode']").val(data_item["ding_mode"]);
    }
    $("#" + t_name + " a[name=link_delete]").each(function () {
        var current_link = $(this);
        var current_tr = current_link.parents("tr");
        var message_tag = current_tr.attr("message_tag");
        current_link.click(function () {
            var show_text = "确定删除消息标签\n" + message_tag;
            swal({
                    title: "确定删除",
                    text: show_text,
                    type: "info",
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: '删除',
                    cancelButtonText: "取消",
                    closeOnConfirm: true,
                    closeOnCancel: true
                },
                function (isConfirm) {
                    if (isConfirm) {
                        var tag_url = $("#tag_url").val();
                        my_async_request2(tag_url, "DELETE", {"message_tag": message_tag}, update_success);
                    }
                }
            );
        });

    });
    $("#" + t_name).find("tr[user_name='" + $("#current_user_name").val() + "']").each(function () {
        var current_tr = $(this);
        var link_delete = $("<a href='javascript:void(0)' name='link_delete'>删除</a>");
        var message_tag = current_tr.attr("message_tag");
        link_delete.click(function () {
            var show_text = "确定删除消息标签\n" + message_tag;
            swal({
                    title: "确定删除",
                    text: show_text,
                    type: "info",
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: '删除',
                    cancelButtonText: "取消",
                    closeOnConfirm: true,
                    closeOnCancel: true
                },
                function (isConfirm) {
                    if (isConfirm) {
                        var tag_url = $("#tag_url").val();
                        my_async_request2(tag_url, "DELETE", {"message_tag": message_tag}, update_success);
                    }
                }
            );
        });
        current_tr.find("td[name='td_op']").append(link_delete);

        current_tr.find("label").children().click(function () {
            var parent_tr = $(this).parents("tr");
            prepare_update(parent_tr);
        });
        current_tr.find("td[name='td_interval_time'] input").change(function () {
                var parent_tr = $(this).parents("tr");
                var match_r = $(this).val().match(/^\d{2,5}$/g);
                if (match_r == null) {
                    $(this).val(parent_tr.attr("interval_time"));
                    return;
                }
                prepare_update(parent_tr);
            }
        );
        current_tr.next().children().change(function () {
            var parent_tr = $(this).parents("tr");
            prepare_update(parent_tr.prev());
        });
        current_tr.find("td[name='td_notify_ding']").click(function () {
                var parent_tr = $(this).parents("tr");
                $("td[name='tr_ding_setting']").hide();
                parent_tr.next().find("td").show();
            }
        );
        current_tr.find("input").removeAttr("disabled");

    });
    $("td[name='tr_ding_setting']").hide();

    var notify_mode = {"notify_email": 1, "notify_wx": 2, "notify_ding": 4};
    for(var i=0;i<data_len;i++){
        var t_item = tags_data[i];
        for (var key in notify_mode)
        {
            t_item[key] = judge_include_value(t_item["notify_mode"], notify_mode[key])
        }
        t_item["add_time"] = timestamp_2_datetime(t_item["insert_time"]);
        t_item.is_owner = $("#current_user_name").val() == t_item.user_name;
        t_item.show = false;
        t_item.is_delete = false;
        //console.info(t_item);
        g_tags_vm.tags.push(t_item);
    }
}

function judge_tr_update(tr_el) {
    var message_tag = tr_el.attr("message_tag");
    var update_info = {"message_tag": message_tag};
    var notify_mode = parseInt(tr_el.attr("notify_mode"));
    var interval_time = tr_el.attr("interval_time");
    var access_ding = tr_el.attr("access_ding");
    var ding_mode = tr_el.attr("ding_mode");
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
    var next_tr = tr_el.next();
    var current_access_ding = format_access_ding(next_tr.find("input[name='access_ding']"));

    var current_ding_mode = next_tr.find("select[name='ding_mode']").val();
    if (current_access_ding != access_ding) {
        console.info(access_ding);
        has_update = true;
        update_info["access_ding"] = current_access_ding;
    }
    if (current_ding_mode != ding_mode) {
        has_update = true;
        update_info["ding_mode"] = current_ding_mode;
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
        //$("div[role='alert']").hide();
        //var dialog_div = $('<div class="alert alert-success" role="alert"></div>');
        //$("body").append(dialog_div);
        //register_reset_bottom(dialog_div);
        //setTimeout(function () {
        //    dialog_div.remove();
        //}, 2000);
        var current_tr = $("tr[message_tag='" + update_data["message_tag"] + "']");
        if (update_data["op"] == "PUT") {
            var msg = "更新消息标签 " + update_data["message_tag"] + " 成功";
            show_msg(msg);
            tag_info_2_tr(update_data, current_tr);
            //dialog_div.text("更新消息标签 " + update_data["message_tag"] + " 成功");
        }
        else {
            var msg = "删除消息标签 " + update_data["message_tag"] + " 成功";
            show_msg(msg);
            current_tr.remove();
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
    if (message_tag.length <= 0) {
        return;
    }
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
        var access_ding = format_access_ding($("#access_ding"));
        var ding_mode = $("#ding_mode").val();
        r_data["access_ding"] = access_ding;
        r_data["ding_mode"] = ding_mode;
    }
    r_data["notify_mode"] = notify_mode;
    var tag_url = $("#tag_url").val();
    my_async_request2(tag_url, "POST", r_data);
}

function show_access_ding() {
    var current_lab = $(this);
    if (current_lab.find("input[name='ding_notify']").is(':checked')) {
        $("#div_ding").show();
    }
    else {
        $("#div_ding").hide();
    }
}

$(document).ready(function () {
    var tag_vm = new Vue({
        el: "#t_tag",
        data: {
            tags: []
        },
        methods: {
            delete_tag: function (index) {
                console.info(index);
                var message_tag = this.tags[index].message_tag;
                var show_text = "确定删除消息标签\n" + message_tag;
                swal({
                        title: "确定删除",
                        text: show_text,
                        type: "info",
                        showCancelButton: true,
                        confirmButtonColor: '#DD6B55',
                        confirmButtonText: '删除',
                        cancelButtonText: "取消",
                        closeOnConfirm: true,
                        closeOnCancel: true
                    },
                    function (isConfirm) {
                        if (isConfirm) {
                            var tag_url = $("#tag_url").val();
                            my_async_request2(tag_url, "DELETE", {"message_tag": message_tag}, function(data){
                                var item = g_tags_vm.tags[index];
                                item.is_delete = true;
                                var msg = "删除消息标签 " + message_tag + " 成功";
                                show_msg(msg);
                            });
                        }
                    }
                );
            },
            show_ding: function(index){
                console.info(index);
                for(var i=0;i<this.tags.length;i++)
                {
                    this.tags[i].show = false;
                }
                this.tags[index].show = true;
            }
        }
    });
    g_tags_vm = tag_vm;
    if ($("#current_user_name").length <= 0) {
        var t_name = "t_tag";
        clear_table(t_name);
        var login_link = $("<a>登录</a>");
        var login_url = "/?next=" + location.href;
        login_link.attr("href", login_url);
        add_row_td(t_name, "未登录").append(login_link);
        $("#btn_new_tag").text("未登录");
        $("#btn_new_tag").click(function () {
            location.href = login_url;
        });
    }
    else {
        var tag_url = $("#tag_url").val();
        my_async_request2(tag_url, "GET", null, handler_tags);
        $("#btn_new_tag").click(add_tag);
        $("#lab_ding_notify").click(show_access_ding);
        $("#interval_time").keyup(function () {
            $("#interval_time").val(format_num($("#interval_time").val()));
        });
        $("#access_ding").change(function () {
            format_access_ding($(this));
        });
    }
});