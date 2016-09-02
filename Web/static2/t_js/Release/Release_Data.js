/**
 * Created by meisanggou on 2016/9/2.
 */

function request_task_list_success(data)
{
    if(data.status == false){
        sweetAlert(data.data);
    }
    var today_task_list = data.data;
    console.info(today_task_list);
}

function request_task_list()
{
    var url_task_list = $("#url_task_list").val();
    my_async_request(url_task_list, "GET", null, request_task_list_success)
}


$(function(){
    request_task_list();
});