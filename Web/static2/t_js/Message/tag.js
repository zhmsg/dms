/**
 * Created by msg on 2/9/17.
 */

var request_tag_flag = new Object();
var g_tags_vm = null;
var can_update_key = ["interval_time", "notify_mode", "access_ding", "ding_mode"];
var notify_mode_dict = {"notify_email": 1, "notify_wx": 2, "notify_ding": 4};

function f_access_ding(v){
    if (v.indexOf("access_token=") >= 0) {
        v = v.substr(v.indexOf("access_token=") + 13);
    }
    return v;
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
    for(var i=0;i<data_len;i++){
        var t_item = tags_data[i];
        for(var j=0;j<can_update_key.length;j++) {
            var key = can_update_key[j];
            t_item["origin_" + key] = t_item[key];
        }
        for (var key in notify_mode_dict) {
            t_item[key] = judge_include_value(t_item["notify_mode"], notify_mode_dict[key])
        }
        t_item["add_time"] = timestamp_2_datetime(t_item["insert_time"]);
        t_item.is_owner = $("#current_user_name").val() == t_item.user_name;
        t_item.show = false;
        t_item.is_delete = false;
        g_tags_vm.all_tags.push(t_item);
    }

    // filter
    for(var i=0;i<g_tags_vm.all_tags.length;i++){
        g_tags_vm.suit_tags.push(i)
    }
    for(var i=0;g_tags_vm.index<g_tags_vm.suit_tags.length&&i<10; g_tags_vm.index++, i++){
        g_tags_vm.tags.push(g_tags_vm.all_tags[g_tags_vm.suit_tags[g_tags_vm.index]]);
    }
    if(g_tags_vm.index >= g_tags_vm.suit_tags.length){
        g_tags_vm.can_load = false;
    }
    else{
        g_tags_vm.can_load = true;
    }

}

function judge_whether_update(index) {
    var now_item = g_tags_vm.tags[index];
    var message_tag = now_item.message_tag;
    console.info(message_tag);
    var update_info = {"message_tag": message_tag};
    var has_update = false;
    var notify_mode = 0;
    for (var key in notify_mode_dict) {
        if (now_item[key] == true) {
            notify_mode += notify_mode_dict[key];
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
            var t_item = g_tags_vm.tags[index];
            for(var j=0;j<can_update_key.length;j++) {
                var key = can_update_key[j];
                t_item["origin_" + key] = t_item[key];
            }
        });
    }
    if (message_tag in request_tag_flag) {
        request_tag_flag[message_tag] = false;
    }
}


$(document).ready(function () {
    var need_login = false;
    var login_url = "/?next=" + location.pathname + location.search;
    if ($("#current_user_name").length <= 0) {
        var need_login = true;
    }
    var tag_vm = new Vue({
        el: "#t_tag",
        data: {
            login_url: login_url,
            need_login: need_login,
            all_tags: [],
            suit_tags: [],
            tags: [],
            can_load: false,
            index: 0
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
            update_action: function(index, format){
                if(format == 1){
                    this.tags[index].access_ding = f_access_ding(this.tags[index].access_ding);
                }
                prepare_update2(index);
            },
            load_more: function(){
                console.info("lode more");
                for(var i=0;g_tags_vm.index<g_tags_vm.suit_tags.length&&i<10; g_tags_vm.index++, i++){
                    g_tags_vm.tags.push(g_tags_vm.all_tags[g_tags_vm.suit_tags[g_tags_vm.index]]);
                }
                if(g_tags_vm.index >= g_tags_vm.suit_tags.length){
                    g_tags_vm.can_load = false;
                }
                else{
                    g_tags_vm.can_load = true;
                }
            }
        }
    });
    g_tags_vm = tag_vm;


    var tag_item = {"message_tag": "", "interval_time": "", "notify_email": false, "notify_wx": false,
        "notify_ding": false, "access_ding": "", "ding_mode": "1"};
    var add_vm = new Vue({
        el: "#div_add_tag",
        data:{
            login_url: login_url,
            need_login: need_login,
            tag_item: tag_item
        },
        methods:{
            action_new: function(){
                var tag_item = this.tag_item;
                var message_tag = tag_item.message_tag;
                if (message_tag.length <= 0) {
                    return;
                }
                var interval_time = tag_item.interval_time;
                var notify_mode = 0;
                var r_data = {"message_tag": message_tag, "interval_time": interval_time};
                for (var key in notify_mode_dict) {
                    if (tag_item[key] == true) {
                        notify_mode += notify_mode_dict[key];
                    }
                }
                r_data["access_ding"] = tag_item.access_ding;
                r_data["ding_mode"] = tag_item.ding_mode;
                r_data["notify_mode"] = notify_mode;
                var tag_url = $("#tag_url").val();
                console.info(r_data);
                my_async_request2(tag_url, "POST", r_data);
            },
            format_ding: function(){
                this.tag_item.access_ding = f_access_ding(this.tag_item.access_ding);
            }
        }

    });
    if (need_login == false) {
        var tag_url = $("#tag_url").val();
        my_async_request2(tag_url, "GET", null, handler_tags);
    }
});