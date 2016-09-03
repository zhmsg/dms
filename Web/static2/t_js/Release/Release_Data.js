/**
 * Created by meisanggou on 2016/9/2.
 */

var has_task = false;
var max_hour = 0;

function timestamp_2_str(timestamp)
{
    var d = new Date(parseInt(timestamp) * 1000);
    var hour = d.getHours();
    var minute = d.getMinutes();
    if(hour > max_hour)
        max_hour = hour;
    return  hour + ":" + minute;
}

function ensure_right_time()
{
    var now_time = new Date();
    var hour = now_time.getHours();
    var minute = now_time.getMinutes();
    $("#btn_add_task").unbind('click');
    if((9<=hour && hour<=11 || 14<=hour && hour<=17) && 10 <= minute &&　minute<=20){
        if(hour <= max_hour)
        {
            $("#btn_add_task").attr("disabled", "disabled");
            $("#btn_add_task").text("已有他人预约");
        }
        else {
            $("#btn_add_task").removeAttr("disabled");
            $("#btn_add_task").click(save_task);
            $("#btn_add_task").text("预约");
        }
    }
    else{
        $("#btn_add_task").attr("disabled", "disabled");
        $("#btn_add_task").text("非预约时段");
    }
    setTimeout(ensure_right_time, 30000);
}

function save_task()
{
    var reason = $("#request_reaseon").val();
    var reason_desc = $("#request_reaseon_desc").val();
    var request_data = new Object();
    request_data["reason"] = reason;
    request_data["reason_desc"] = reason_desc;
    var url_task = $("#url_task_list").val();
    my_async_request(url_task, "POST", request_data, request_task_list);
}

function request_task_list_success(data)
{
    if(data.status == false){
        sweetAlert(data.data);
    }
    var today_task_list = data.data;
    for(var i=0;i<today_task_list.length;i++){
        var status_list = new Array();
        var status_s_list = today_task_list[i].status_info.split("|");
        var j = 0;
        for(;j<status_s_list.length;j++)
        {
            var status_item = status_s_list[j];
            status_list[j] = new Object();
            status_list[j].time = timestamp_2_str(status_item.substr(0, status_item.length - 1));
            if(status_item[status_item.length - 1] == "0")
            {
                status_list[j].result = false;
            }
            else
            {
                status_list[j].result = true;
            }
        }
        for(;j < 5; j++){
            status_list[j] = null;
        }
        today_task_list[i].status_list = status_list;
        Add_Task_Info(today_task_list[i]);
    }
    ensure_right_time();
}

function request_task_list(data)
{
    if(data==null || data.status==true) {
        var url_task_list = $("#url_task_list").val();
        my_async_request(url_task_list, "GET", null, request_task_list_success)
    }
    else
    {
        sweetAlert(data.data);
    }
}


$(function(){
    request_task_list();
});