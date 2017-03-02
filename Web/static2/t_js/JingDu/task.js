/**
 * Created by msg on 2/9/17.
 */

var query_task_ing = new Object({"exec_r": null, "exec_completed": false, "exec_ing": false});


function show_task_info(task_data){
    console.info(task_data);
    //
    var task_len = task_data.length;
    var t_name = "t_user_task";
    clear_table(t_name);
    var t_task = $("#" + t_name);
    var keys = ["task_id", "account", "app_id", "input", "output", "status", "started_stamp", "duration"];
    var now_stamp = get_timestamp();
    for(var i=0;i<task_len;i++){
        var task_item = task_data[i];
        if(task_item["finished_stamp"] != null){
            task_item["duration"] = duration_show(task_item["finished_stamp"] - task_item["started_stamp"]);
        }
        else{
            task_item["duration"] = duration_show(now_stamp - task_item["started_stamp"]);
        }
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
    });
    //$("td[name='td_completed']:visible").each(function(){
    //    var current_td = $(this);
    //    if(current_td.text() == "false"){
    //        current_td.text("未完成");
    //    }
    //    else{
    //        current_td.text("已完成");
    //    }
    //});
    //$("a[name='td_look_partner']:visible").each(function(){
    //    var current_td = $(this);
    //    current_td.unbind("click");
    //    current_td.click(click_look_partner);
    //});
}

function query_task(){
    if(query_task_ing.exec_ing == true){
        return;
    }
    query_task_ing.exec_ing = true;
    query_task_ing.exec_completed = false;
    var request_url = "task/";
    var started_stamp = today_timestamp();
    console.info(started_stamp);
    my_async_request2(request_url, "GET", {"started_stamp": started_stamp}, show_task_info, query_task_ing);
}


$(document).ready(function () {
    $("#link_today_task").click(query_task);
});