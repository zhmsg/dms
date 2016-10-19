/**
 * Created by msg on 11/3/15.
 */

function add_header_success(data)
{
    if (data.status == true){
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
    else{
        alert(data)
    }
}

function add_body_success(data)
{
    if (data.status == true){
        var new_data = data.data;
        for(var i=0;i<new_data.length;i++){
            var param = new_data[i].param;
            $("#trb_" + new_data[i].api_no + new_data[i].param).remove();
            var trHTML = "<tr id='trb_" + new_data[i].api_no + new_data[i].param + "'><td>" + new_data[i].param;
            trHTML += '</td><td>';
            if (new_data[i].necessary == true) {
                trHTML += '是';
            }
            else{
                trHTML += '否';
            }
            trHTML += '<td>' + new_data[i].type + '</td><td>' + new_data[i].desc + '</td>';
            trHTML += '<td><button class="btn btn-success" onclick="update_body_param(' + "'" + api_no + "','" + param + "'" + ')">更新</button>';
            trHTML += '<button class="btn btn-danger"  onclick="delete_body_param('+ "'" + new_data[i].api_no + "','" + new_data[i].param + "'" + ')">删除</button></td></tr>"';
            var tr=$("#api_body_param tr").eq(-2);
            tr.after(trHTML);
        }
        $("#body_param_name").val("");
        $("#body_param_desc").val("");
        $("#body_param_type").val("");
        $("#btn_new_body").text("新建");

        $("#btn_new_body").removeClass();
        $("#btn_new_body").addClass("btn btn-info");
    }
}

function add_input_success(data)
{
    if (data.status == true) {
        var new_data = data.data;
        for(var i=0;i<new_data.length;i++) {
            var div_html = '<div id="div_' + new_data[i].input_no + '"><p>' + new_data[i].desc +'</p><p><textarea class="form-control" readonly>' + new_data[i].example + '</textarea></p>';
            div_html += '<button class="btn btn-success">更新</button> <button class="btn btn-danger" onclick="delete_input_param(' + "'" + new_data[i].input_no + "'" + ')">删除</button></div>';
            $("#api_input_exist").append(div_html);
        }
        $("#input_param_desc").val("");
        $("#input_param_example").val("");
    }
    else{
        alert(data);
    }
}

function add_output_success(data)
{
    if (data.status == true) {
        var new_data = data.data;
        for(var i=0;i<new_data.length;i++) {
            var div_html = '<div id="div_' + new_data[i].output_no + '"><p>' + new_data[i].desc +'</p><p><textarea class="form-control" readonly>' + new_data[i].example + '</textarea></p>'
            div_html += '<button class="btn btn-success">更新</button> <button class="btn btn-danger" onclick="delete_output_param(' + "'" + new_data[i].output_no + "'" + ')">删除</button></div>';
            $("#api_output_exist").append(div_html);
        }
        $("#output_param_desc").val("");
        $("#output_param_example").val("");
    }
    else{
        alert(data);
    }
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
        my_async_request(request_url, "POST", request_data, add_body_success);
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

function delete_body_param(api_no, param){
    var del_url = $("#del_body_url").val();
    var request_data = JSON.stringify({"api_no": api_no, "param": param});
    $.ajax({
        url: del_url,
        method: "DELETE",
        contentType: "application/json",
        data: request_data,
        success:function(data){
            if (data.status == true){
                $("#trb_"+api_no + param).remove();
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

function handle_predefine_param(btn_id, param_type){
    var update_url = $("#update_header_url").val();
    var btn = $("#" + btn_id);
    console.info(btn);
    var inner_value = btn.text();
    console.info(inner_value);
    var param = btn.val();
    console.info(param);
    if(inner_value.indexOf("不需要") == 0){
        var class_name = "btn btn-info";
        var inner_value = inner_value.replace("不", "");
        var update_type = "delete";
    }
    else{
        var class_name = "btn btn-danger";
        var inner_value = inner_value.replace("需要", "不需要");
        var update_type = "new";
    }
    $.ajax({
        url: update_url,
        method: "PUT",
        data: {param: param, update_type: update_type, param_type: param_type},
        success:function(data){
            if (data.status == true){
                btn.text(inner_value);
                btn.removeClass();
                btn.addClass(class_name);
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

function update_body_param(api_no, param)
{
    var param_tr = $("#trb_" + api_no + param);
    var tds = param_tr.find("td");
    $("#body_param_name").val(tds[0].innerHTML);
    setSelectChecked("body_param_necessary", tds[1].innerHTML);
    setSelectChecked("body_param_type", tds[2].innerHTML);
    $("#body_param_desc").val(tds[3].innerHTML);
    $("#btn_new_body").text("更新");
    $("#btn_new_body").removeClass();
    $("#btn_new_body").addClass("btn btn-success");
}

$(function(){
    var status = $("#api_status").val();
    if(status == "新建" || status == "修改中"){
        $("#span_modify_status").append('<a class="margin10" href="/dev/api/status/2/">设置完成</a>');
        $("#span_modify_status").append('<a class="margin10" href="/dev/api/status/3/">设置待废弃</a>');
    }
    else if(status == "已完成")
    {
        $("#span_modify_status").append('<a class="margin10" href="/dev/api/status/1/">设置修改中</a>');
        $("#span_modify_status").append('<a class="margin10" href="/dev/api/status/3/">设置待废弃</a>');

    }
    else{

    }
    $("#span_modify_status").append('<a class="margin10" href="/dev/api/status/4/">设置废弃</a>');
});