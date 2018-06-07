/**
 * Created by msg on 2/9/17.
 */

var request_tag_flag = new Object();
var g_tags_vm = null;
var can_update_key = ["interval_time", "notify_mode", "access_ding", "ding_mode"];

function format_access_ding(el) {
    var current_access_ding = el.val();
    if (current_access_ding.indexOf("access_token=") >= 0) {
        current_access_ding = current_access_ding.substr(current_access_ding.indexOf("access_token=") + 13);
        el.val(current_access_ding);
    }
    return current_access_ding;
}

function prepare_update2(index)
{
    //  判断是否和已有的有变化
    var update_info = judge_whether_update(index);
    if (update_info != null) {
        var message_tag = update_info["message_tag"];
        if (message_tag in request_tag_flag && request_tag_flag[message_tag] == true) {
            console.info("wait ...");
        }
        else {
            request_tag_flag[message_tag] = true;
            window.setTimeout(function () {
                start_update_tag2(index);
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
    var notify_mode = {"notify_email": 1, "notify_wx": 2, "notify_ding": 4};
    for(var i=0;i<data_len;i++){
        var t_item = tags_data[i];
        for(var j=0;j<can_update_key.length;j++) {
            var key = can_update_key[j];
            t_item["origin_" + key] = t_item[key];
        }
        for (var key in notify_mode) {
            t_item[key] = judge_include_value(t_item["notify_mode"], notify_mode[key])
        }
        t_item["add_time"] = timestamp_2_datetime(t_item["insert_time"]);
        t_item.is_owner = $("#current_user_name").val() == t_item.user_name;
        t_item.show = false;
        t_item.is_delete = false;
        g_tags_vm.tags.push(t_item);
    }
}

function judge_whether_update(index) {
    var now_item = g_tags_vm.tags[index];
    var message_tag = now_item.message_tag;
    console.info(message_tag);
    var update_info = {"message_tag": message_tag};
    var has_update = false;
    var notify_mode_dict = {"notify_email": 1, "notify_wx": 2, "notify_ding": 4};
    var notify_mode = 0;
    for (var key in notify_mode_dict) {
        if (now_item[key] == true) {
            notify_mode += notify_mode_dict[key]
        }
    }
    now_item.notify_mode = notify_mode;
    for(var i=0;i<can_update_key.length;i++)
    {
        var key = can_update_key[i];
        if(now_item[key] != now_item["origin_" + key]){
            update_info[key] = now_item[key];
            has_update = true;
        }
    }
    if (has_update == false) {
        return null;
    }
    else {
        return update_info
    }
}



function start_update_tag2(index) {
    console.info("start update tag");
    var message_tag = g_tags_vm.tags[index].message_tag;
    var update_info = judge_whether_update(index);
    if (update_info == null) {
        console.info("no update info");
    }
    else {
        var tag_url = $("#tag_url").val();
        my_async_request2(tag_url, "PUT", update_info, function(data){
            var msg = "更新消息标签 " + message_tag + " 成功";
            show_msg(msg);
        });
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
                for(var i=0;i<this.tags.length;i++)
                {
                    this.tags[i].show = false;
                }
                this.tags[index].show = true;
            },
            update_action: function(index){
                prepare_update2(index);
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