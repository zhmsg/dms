/**
 * Created by meisanggou on 2016/9/2.
 */


function ensure_right_time()
{
    var now_time = new Date();
    var hour = now_time.getHours();
    var minute = now_time.getMinutes();
    $("#btn_add_task").unbind('click');
    if(hour <= max_hour)
    {
        $("#btn_add_task").attr("disabled", "disabled");

        if(max_owner == current_user){
            $("#btn_add_task").text("已预约本时段");
        }
        else {
            $("#btn_add_task").text("已有他人预约");
        }
    }
    else if(book_num >= 2)
    {
        $("#btn_add_task").attr("disabled", "disabled");
        $("#btn_add_task").text("今日已预约2次");
    }
    else {
        if($("#request_service").val() != "") {
            $("#btn_add_task").removeAttr("disabled");
            $("#btn_add_task").click(save_task);
            $("#btn_add_task").text("预约");
        }
        else
        {
            $("#btn_add_task").attr("disabled", "disabled");
            $("#btn_add_task").text("请选择服务");
        }
    }
    setTimeout(ensure_right_time, 30000);
}