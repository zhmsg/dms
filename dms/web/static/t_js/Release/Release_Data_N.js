/**
 * Created by meisanggou on 2016/9/2.
 */


function ensure_right_time()
{
    var now_time = new Date();
    var hour = now_time.getHours();
    var minute = now_time.getMinutes();
    var week_day = now_time.getDay();
    $("#btn_add_task").unbind('click');
    // 周三 14-18 周四 8-12 14-16
    // 10分-20分
    if (((week_day == 3 && 14 <= hour && hour<= 18) || ( week_day == 4 && (8 <= hour && hour <= 12 || 14 <= hour && hour <= 16))) && 10 <= minute && minute < 20) {
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
    }
    else{
        $("#btn_add_task").attr("disabled", "disabled");
        $("#btn_add_task").text("非预约时段");
    }
    setTimeout(ensure_right_time, 30000);
}