/**
 * Created by msg on 2/9/17.
 */

var query_task_ing = new Object({"exec_r": null, "exec_completed": false, "exec_ing": false});


function click_task_id(){
    var task_id = $(this).attr("title");
    console.info(task_id);
    copy_text(task_id);
}

var app_storage_key = "app_list";

function show_task_info(task_data){
    var task_len = task_data.length;
    var t_name = "t_user_task";
    clear_table(t_name);
    var t_task = $("#" + t_name);
    var keys = ["task_id", "account", "app_id", "input", "output", "status", "db_status", "started_stamp", "duration"];
    var now_stamp = get_timestamp2();
    if(task_len == 0){
        add_row_td(t_name, "无任务");
    }
    for(var i=0;i<task_len;i++){
        var task_item = task_data[i];
        if(task_item["finished_stamp"] != null){
            task_item["duration"] = duration_show(task_item["finished_stamp"] - task_item["started_stamp"]);
        }
        else{
            task_item["duration"] = duration_show(now_stamp - task_item["started_stamp"]);
        }
        task_item["started_stamp"] = timestamp_2_datetime(task_item["started_stamp"]);
        var add_tr = $("<tr></tr>");
        for(var j=0;j<keys.length;j++){
            var one_td = new_td(keys[j], task_item);
            add_tr.append(one_td);
        }
        t_task.append(add_tr);
    }
    $("td[name='td_task_id']:visible").each(function(){
        var current_td = $(this);
        var task_id = current_td.text();
        var show_id = task_id.substr(0, 3) + "***" + task_id.substr(28, 4);
        current_td.text(show_id);
        current_td.attr("title", task_id);
        current_td.addClass("status_move");
        current_td.click(click_task_id);
    });
    var app_data = sessionStorage.getItem(app_storage_key);
    if(app_data != null){
        handler_app(JSON.parse(app_data), true);
    }
    else {
        var request_url = "app/";
        my_async_request2(request_url, "GET", null, handler_app);
    }
}


function handler_app(app_data, from_cache){
    if(from_cache == null) {
        console.info("save app data to session storage");
        sessionStorage.setItem(app_storage_key, JSON.stringify(app_data));
    }
    var app_len = app_data.length;
    var app_data_d = new Object();
    for(var i=0;i<app_len;i++){
        var app_item = app_data[i];
        app_item["status_desc"] = app_item["status_desc"].split(",");
        app_data_d["" + app_item["app_id"]] = app_item;
    }
    $("td[name='td_app_id']").each(function(){
        var current_td = $(this);
        var app_id = current_td.text();
        if(app_id in app_data_d){
            current_td.text(app_data_d[app_id]["app_name"]);
        }
        var status_td = current_td.nextAll("[name='td_status']");
        var status_s = status_td.text();
        var status = parseInt(status_s);
        if(app_id.length >=3)
            status = status - 1;
        status_td.text(status_s + "-" + app_data_d[app_id]["status_desc"][status]);
    });
}

function query_task(){
    if(query_task_ing.exec_ing == true){
        return;
    }
    query_task_ing.exec_ing = true;
    query_task_ing.exec_completed = false;
    var request_url = "task/";
    var started_stamp = today_timestamp();
    my_async_request2(request_url, "GET", {"started_stamp": started_stamp}, show_task_info, query_task_ing);
}


$(document).ready(function () {
    $("#link_today_task").click(query_task);
});