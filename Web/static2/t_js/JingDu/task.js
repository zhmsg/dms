/**
 * Created by msg on 2/9/17.
 */

var query_task_ing = new Object({"exec_r": null, "exec_completed": false, "exec_ing": false});


function click_task_id(){
    var task_id = $(this).attr("title");
    console.info(task_id);
    copy_text(task_id);
}

function show_task_info(task_data){
    var task_len = task_data.length;
    var t_name = "t_user_task";
    clear_table(t_name);
    var t_task = $("#" + t_name);
    var keys = ["task_id", "account", "app_id", "input", "output", "status", "db_status", "started_stamp", "duration"];
    var now_stamp = get_timestamp2();
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
    window.onresize = function() {
        reset_bottom();
    }
    function reset_bottom()
    {
        $("div[name='pop_div']").each(function(){
            var div_el = $(this);
            div_el.show();
            var height = $(window).height();
            var width = $(window).width();
            div_el.css({'left': (width / 2 - div_el.width() / 2) + "px", 'top': (height - div_el.height() - 40) + 'px'});
        });
        $("div[name='pop_div1']").each(function(){
            var div_el = $(this);
            div_el.show();
            var height = $(window).height();
            var width = $(window).width();
            div_el.css({'left': (width / 2 - div_el.width() / 2) + "px", 'top': (height - div_el.height() - 140) + 'px'});
        });
    }
    reset_bottom();
});