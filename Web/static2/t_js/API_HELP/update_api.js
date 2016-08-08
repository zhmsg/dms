/**
 * Created by msg on 11/3/15.
 */

function new_header_param(new_url){
    var api_no = $("#api_no").val();
    var param = $("#header_param_name").val();
    var necessary = $("#header_param_ne").val();
    var desc = $("#header_param_desc").val();
    $.ajax({
        url: new_url,
        method: "POST",
        data:{param:param,necessary:necessary,desc:desc,api_no:api_no},
        success:function(data){
            if (data.status == true){
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
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}

function new_body_param(new_url){
    var api_no = $("#api_no").val();
    var param = $("#body_param_name").val();
    var necessary = $("#body_param_ne").val();
    var type = $("#body_param_type").val();
    var desc = $("#body_param_desc").val();
    $.ajax({
        url: new_url,
        method: "POST",
        data:{param:param,necessary:necessary,desc:desc,api_no:api_no, type:type},
        success:function(data){
            if (data.status == true){
                var new_data = data.data;
                for(var i=0;i<new_data.length;i++){
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
                $("#body_param_new").text("新建");

                $("#body_param_new").removeClass();
                $("#body_param_new").addClass("btn btn-info");
            }
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}

function new_input_example(new_url){
    var api_no = $("#api_no").val();
    var desc = $("#input_desc").val();
    var example = $("#input_example").val();
    $.ajax({
        url: new_url,
        method: "POST",
        data:{desc:desc,api_no:api_no,example:example},
        success:function(data){
            if (data.status == true) {
                var new_data = data.data;
                for(var i=0;i<new_data.length;i++) {
                    var div_html = '<div id="div_' + new_data[i].input_no + '"><p>' + new_data[i].desc +'</p><p><textarea class="form-control" readonly>' + new_data[i].example + '</textarea></p>'
                    div_html += '<button class="btn btn-success">更新</button> <button class="btn btn-danger" onclick="delete_input_param(' + "'" + new_data[i].input_no + "'" + ')">删除</button></div>';
                    $("#api_input_exist").append(div_html);
                }
                $("#input_desc").val("");
                $("#input_example").val("");
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

function new_output_example(new_url){
    var api_no = $("#api_no").val();
    var desc = $("#output_desc").val();
    var example = $("#output_example").val();
    $.ajax({
        url: new_url,
        method: "POST",
        data:{desc:desc,api_no:api_no,example:example},
        success:function(data){
            if (data.status == true) {
                var new_data = data.data;
                for(var i=0;i<new_data.length;i++) {
                    var div_html = '<div id="div_' + new_data[i].output_no + '"><p>' + new_data[i].desc +'</p><p><textarea class="form-control" readonly>' + new_data[i].example + '</textarea></p>'
                    div_html += '<button class="btn btn-success">更新</button> <button class="btn btn-danger" onclick="delete_output_param(' + "'" + new_data[i].output_no + "'" + ')">删除</button></div>';
                    $("#api_output_exist").append(div_html);
                }
                $("#output_desc").val("");
                $("#output_example").val("");
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
    setSelectChecked("body_param_ne", tds[1].innerHTML);
    setSelectChecked("body_param_type", tds[2].innerHTML);
    $("#body_param_desc").val(tds[3].innerHTML);
    $("#body_param_new").text("更新");
    $("#body_param_new").removeClass();
    $("#body_param_new").addClass("btn btn-success");
}