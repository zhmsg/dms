/**
 * Created by meisanggou on 2016/9/2.
 */
var step_desc = new Array("预约成功", "发布中", "发布完成", "测试成功", "提交成功");

var url_start_success = $("#url_start_success").val();
var url_middle_success = $("#url_middle_success").val();
var url_end_success = $("#url_end_success").val();

var url_start_gray = $("#url_start_gray").val();
var url_middle_gray = $("#url_middle_gray").val();
var url_end_gray = $("#url_end_gray").val();


function New_Div_Step(step_info, index, is_start, is_end)
{
    var div_one = $('<div class="pull-left market"></div>');
    var img_one = $('<img></img>');
    var img_path;
    if(step_info == null)
    {
        if(is_start == true){
            img_path = url_start_gray;
        }
        else if(is_end == true){
            img_path = url_end_gray;
        }
        else{
            img_path = url_middle_gray;
        }
        img_one.attr('src', img_path);
        div_one.append(img_one);
        var p_one = $("<p></p>");
        p_one.append(step_desc[index]);
        div_one.append(p_one);
    }
    else {
        var img_path = url_middle_success;
        if (step_info.result == true) {
            if (is_start == true)
                img_path = url_start_success;
            else if (is_end == true)
                img_path = url_end_success;
        }
        else{
            if (is_start == true)
                img_path = url_start_success;
            else if (is_end == true)
                img_path = url_end_success;
        }
        img_one.attr('src', img_path);
        div_one.append(img_one);
        var p_one = $("<p></p>");
        p_one.append(step_desc[index]);
        p_one.append("<br />");
        p_one.append(step_info.time);
        div_one.append(p_one);
    }
    return div_one;
}

function Add_Task_Info(task_info)
{
    if(task_info == null)
    {
        $("#div_task_list").text("");
        return;
    }
    var h_user_name = $("<h4></h4>").text(task_info.user_name);
    var h_reason = $("<p></p>").text(task_info.reason);
    var top_color = "#ff991d";
    if(task_info["restart_service"] == 1){
        top_color = "#aa772c"
    }
    else if(task_info["restart_service"] == 2){
        top_color = "#66553b"
    }
    var div_left = $('<div class="pull-left number" style="border-top: 5px solid ' + top_color + '"></div>');
    div_left.append(h_user_name);
    div_left.append(h_reason);
    $("#div_task_list").append(div_left);

    var div_step = $('<div class="step"></div>');
    div_step.append(New_Div_Step(task_info.status_list[0], 0, true, false));
    for(var i= 1;i < 4;i++){
        div_step.append(New_Div_Step(task_info.status_list[i], i));
    }
    div_step.append(New_Div_Step(task_info.status_list[4], 4, false, true));
    $("#div_task_list").append(div_step);
    $("#div_task_list").append('<div class="clear"></div>');

}