/**
 * Created by meisanggou on 2016/9/2.
 */
function timestamp_2_str(timestamp)
{
    var d = new Date(parseInt(timestamp) * 1000);
    var hour = d.getHours();
    var minute = d.getMinutes();
    return  hour + ":" + minute;
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
}

function request_task_list()
{
    var url_task_list = $("#url_task_list").val();
    my_async_request(url_task_list, "GET", null, request_task_list_success)
}


$(function(){
    request_task_list();
});