/**
 * Created by msg on 11/3/15.
 */

function add_header_success(data)
{
    var new_data = data.data;
    for(var i=0;i<new_data.length;i++){
        var t_len = $("#api_header_param").length;
        var trHTML = "<tr id='tr_" + new_data[i].api_no + new_data[i].param + "'><td>" + new_data[i].param;
        trHTML += '</td><td><select class="form-control" disabled>';
        if (new_data[i].necessary == true) {
            trHTML += '<option value="1" selected="selected">是</option><option value="0">否</option></select></td>';
        }
        else{
            trHTML += '<option value="1">是</option><option value="0" selected="selected">否</option></select></td>';
        }
        trHTML += '<td>' + new_data[i].desc + '</td><td><button class="btn btn-success">更新</button> <button class="btn btn-danger"  onclick="delete_header_param('+ "'" + new_data[i].api_no + "','" + new_data[i].param + "'" + ')">删除</button></td></tr>"';
        var tr=$("#api_header_param tr").eq(-2);
        tr.after(trHTML);
    }
    $("#header_param_name").val("");
    $("#header_param_desc").val("");
}

function add_body_success(data)
{
    var tr_id = "trb_" + data.api_no + data.param;
    $("#" + tr_id).remove();
    var add_tr = $("<tr></tr>");
    add_tr.attr("id", tr_id);

    var param_td = $("<td></td>");
    param_td.text(data.param);

    var necessary_td = $("<td></td>");
    if (data.necessary == true) {
        necessary_td.text("是");
    }
    else {
        necessary_td.text("否");
    }

    var type_td = $("<td></td>");
    type_td.text(data.type);

    var desc_td = $("<td></td>");
    desc_td.text(data.param_desc);

    var status_td = $("<td></td>");
    status_td.text(["稍后", "立即", "待废弃", "废弃"][data.status]);

    var op_td = $("<td></td>");
    var up_btn = $("<button class='btn btn-success'>更新</button>");
    var del_btn = $("<button class='btn btn-danger'>删除</button>");
    up_btn.click(update_body_param);
    del_btn.click(delete_body_param);
    op_td.append(up_btn);
    op_td.append(del_btn);

    add_tr.append(param_td);
    add_tr.append(necessary_td);
    add_tr.append(type_td);
    add_tr.append(desc_td);
    add_tr.append(status_td);
    add_tr.append(op_td);
    var tr = $("#api_body_param tr").eq(-2);
    tr.after(add_tr);
    $("#body_param_name").val("");
    $("#body_param_desc").val("");
    $("#body_param_type").val("");
    $("#btn_new_body").text("新建");

    $("#btn_new_body").removeClass();
    $("#btn_new_body").addClass("btn btn-info");
}

function add_input_success(data)
{
    var new_data = data.data;
    for(var i=0;i<new_data.length;i++) {
        var div_html = '<div id="div_' + new_data[i].input_no + '"><p>' + new_data[i].desc +'</p><p><textarea class="form-control" readonly>' + new_data[i].example + '</textarea></p>';
        div_html += '<button class="btn btn-success">更新</button> <button class="btn btn-danger" onclick="delete_input_param(' + "'" + new_data[i].input_no + "'" + ')">删除</button></div>';
        $("#api_input_exist").append(div_html);
    }
    $("#input_param_desc").val("");
    $("#input_param_example").val("");

}

function add_output_success(data)
{
    var new_data = data.data;
    for(var i=0;i<new_data.length;i++) {
        var div_html = '<div id="div_' + new_data[i].output_no + '"><p>' + new_data[i].desc +'</p><p><textarea class="form-control" readonly>' + new_data[i].example + '</textarea></p>'
        div_html += '<button class="btn btn-success">更新</button> <button class="btn btn-danger" onclick="delete_output_param(' + "'" + new_data[i].output_no + "'" + ')">删除</button></div>';
        $("#api_output_exist").append(div_html);
    }
    $("#output_param_desc").val("");
    $("#output_param_example").val("");
}

function add_api_info(type){
    var request_url = $("#url_prefix").val() + "/" + type + "/";
    var id_prefix = type + "_param_";
    var post_params = $("[id^="+ id_prefix +"]");
    var request_data = new Object();
    for(var i=0;i<post_params.length;i++){
        var one_param = post_params[i];
        request_data[one_param.id.substring(id_prefix.length)] = one_param.value;
    }
    if(type == "header")
        my_async_request(request_url, "POST", request_data, add_header_success);
    else if (type == "body")
        my_async_request2(request_url, "POST", request_data, add_body_success);
    else if(type == "input")
        my_async_request(request_url, "POST", request_data, add_input_success);
    else if(type == "output")
        my_async_request(request_url, "POST", request_data, add_output_success);
    console.info(request_data);
}

function delete_header_param(api_no, param){
    var del_url = $("#del_header_url").val();
    var request_data = JSON.stringify({"api_no": api_no, "param": param});
    $.ajax({
        url: del_url,
        data: request_data,
        contentType: "application/json",
        method: "DELETE",
        success:function(data){
            if (data.status == true){
                $("#tr_"+api_no + param).remove();
            }
            else{
                alert(data);
            }
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}

function delete_body_param() {
    var parent_tr = $(this).parent().parent();
    var tds = parent_tr.find("td");
    var param = tds[0].innerHTML;
    var del_url = $("#del_body_url").val();
    var request_data = JSON.stringify({"param": param});
    $.ajax({
        url: del_url,
        method: "DELETE",
        contentType: "application/json",
        data: request_data,
        success:function(data){
            if (data.status == true){
                parent_tr.remove();
            }
            else{
                alert(data);
            }
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}

function delete_example() {

}
function delete_input_param(input_no){
    var del_url = $("#del_input_url").val();
    $.ajax({
        url: del_url + input_no + "/",
        method: "DELETE",
        success:function(data){
            if (data.status == true){
                $("#div_"+input_no).remove();
            }
            else{
                alert(data);
            }
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}

function delete_output_param(output_no){
    var del_url = $("#del_output_url").val();
    $.ajax({
        url: del_url + output_no + "/",
        method: "DELETE",
        success:function(data){
            if (data.status == true){
                $("#div_"+output_no).remove();
            }
            else{
                alert(data);
            }
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}

function format_input(input_id){
    var input_content = $("#" + input_id).val();
    var json_content = JSON.stringify(JSON.parse(input_content), null, 4);
    $("#" + input_id).val(json_content);
}

function handler_success(data){
    var btn_id = "pp_" + data.data["param"];
    var btn = $("#" + btn_id);
    var inner_value = btn.text();
    if(inner_value.indexOf("不需要") == 0){
        var class_name = "btn btn-info";
        var inner_value = inner_value.replace("不", "");
    }
    else{
        var class_name = "btn btn-danger";
        var inner_value = inner_value.replace("需要", "不需要");
    }
    btn.text(inner_value);
    btn.removeClass();
    btn.addClass(class_name);
}

function handle_predefine_param(btn_id, param_type){
    var update_url = $("#url_prefix").val() + "/" + param_type + "/";
    var btn = $("#" + btn_id);
    var inner_value = btn.text();
    var param = btn.val();
    if(inner_value.indexOf("不需要") == 0){
        var update_type = "delete";
    }
    else{
        var update_type = "new";
    }
    my_async_request(update_url, "PUT", {param: param, update_type: update_type, param_type: param_type}, handler_success);
}

function send_message()
{
    alert("即将离开");
}

function setSelectChecked(selectId, checkValue){
    var select = document.getElementById(selectId);
    for(var i=0; i<select.options.length; i++){
        if(select.options[i].innerHTML == checkValue){
            select.options[i].selected = true;
            break;
        }
    }
}

function update_body_param()
{
    var parent_tr = $(this).parent().parent();
    var tds = parent_tr.find("td");
    $("#body_param_name").val(tds[0].innerHTML);
    setSelectChecked("body_param_necessary", tds[1].innerHTML);
    setSelectChecked("body_param_type", tds[2].innerHTML);
    $("#body_param_desc").val(tds[3].innerHTML);
    setSelectChecked("body_param_status", tds[4].innerHTML);
    $("#btn_new_body").text("更新");
    $("#btn_new_body").removeClass();
    $("#btn_new_body").addClass("btn btn-success");
}

function update_stage(stage){
    var update_url = $("#update_stage_url").val();
    my_async_request(update_url, "PUT", {"stage": stage});
}

function add_example(data, sign) {
    var add_div = $("<div></div>");
    var desc_p = $("<p></p>");
    desc_p.text(data[sign + "_desc"]);
    var example_p = $('<p><textarea class="form-control" readonly>' + data[sign + "_example"] + '</textarea></p>');
    var btn_update = $('<p><button class="btn btn-success">更新</button>');
    var btn_del = $('<button class="btn btn-danger">删除</button></p>');
    //onclick="delete_output_param('{{ item["output_no"] }}')
    add_div.append(desc_p);
    add_div.append(example_p);
    add_div.append(btn_update);
    $("#api_" + sign + "_exist").append(add_div);
}

function init_api_info(data) {
    if (data == null) {
        my_async_request2(location.href, "GET", null, init_api_info);
        return;
    }
    var api_info = data.api_info;

    console.info(api_info);
    // basic info
    var keys = ["api_title", "api_url", "api_method", "api_desc", "stage", "add_time", "update_time"];
    var key_len = keys.length;
    for (var i = 0; i < key_len; i++) {
        $("#span_" + keys[i]).text(api_info.basic_info[keys[i]]);
    }
    // body
    var body_len = api_info.body_info.length;
    for (var i = 0; i < body_len; i++) {
        add_body_success(api_info.body_info[i]);
    }
    // input
    var input_len = api_info.input_info.length;
    for (var i = 0; i < input_len; i++) {
        var input_item = api_info.input_info[i];
        add_example(input_item, "input");
    }
    // output
    var output_len = api_info.output_info.length;
    for (var i = 0; i < output_len; i++) {
        var output_item = api_info.output_info[i];
        add_example(output_item, "output");
    }
}

$(function(){
    init_api_info();
    var stage = $("#api_stage").val();
    var update_url = $("#update_stage_url").val();
    if(stage == "新建" || stage == "修改中"){
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(2);">设置完成</a>');
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(3);">设置待废弃</a>');
    }
    else if(stage == "已完成")
    {
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(1);">设置修改中</a>');
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(3);">设置待废弃</a>');

    }
    if (stage != "已废弃" && stage != "已删除") {
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(4);">设置废弃</a>');
    }
});