/**
 * Created by msg on 11/3/15.
 */

function new_header_param(){
    var api_no = $("#api_no").val();
    var param = $("#header_param_name").val();
    var necessary = $("#header_param_ne").val();
    var desc = $("#header_param_desc").val();
    $.ajax({
        url: "/dev/api/add/header/",
        method: "POST",
        data:{param:param,necessary:necessary,desc:desc,api_no:api_no},
        success:function(data){
            var json_obj = JSON.parse(data);
            if (json_obj.status == true){
                var new_data = json_obj.data;
                for(var i=0;i<new_data.length;i++){
                    var t_len = $("#api_header_param").length;
                    var trHTML = "<tr><td>" + new_data[i].param;
                    trHTML += '</td><td><select class="form-control" disabled>'
                    if (new_data[i].necessary == true) {
                        trHTML += '<option value="1" selected="selected">是</option><option value="0">否</option></select></td>';
                    }
                    else{
                        trHTML += '<option value="1">是</option><option value="0" selected="selected">否</option></select></td>';
                    }
                    trHTML += '<td>' + new_data[i].desc + '</td><td><button class="btn btn-success">更新</button> <button class="btn btn-danger">删除</button></td></tr>"';
                    var tr=$("#api_header_param tr").eq(-2);
                    tr.after(trHTML);
                }
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

function new_body_param(){
    var api_no = $("#api_no").val();
    var param = $("#body_param_name").val();
    var necessary = $("#body_param_ne").val();
    var type = $("#body_param_type").val();
    var desc = $("#body_param_desc").val();
    $.ajax({
        url: "/dev/api/add/body/",
        method: "POST",
        data:{param:param,necessary:necessary,desc:desc,api_no:api_no, type:type},
        success:function(data){
            var json_obj = JSON.parse(data);
            if (json_obj.status == true){
                var new_data = json_obj.data;
                for(var i=0;i<new_data.length;i++){
                    var trHTML = "<tr><td>" + new_data[i].param;
                    trHTML += '</td><td><select class="form-control" disabled>'
                    if (new_data[i].necessary == true) {
                        trHTML += '<option value="1" selected="selected">是</option><option value="0">否</option></select></td>';
                    }
                    else{
                        trHTML += '<option value="1">是</option><option value="0" selected="selected">否</option></select></td>';
                    }
                    trHTML += '<td>' + new_data[i].type + '</td><td>' + new_data[i].desc + '</td><td><button class="btn btn-success">更新</button> <button class="btn btn-danger">删除</button></td></tr>"';
                    var tr=$("#api_body_param tr").eq(-2);
                    tr.after(trHTML);
                }
            }
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}

function new_input_example(){
    var api_no = $("#api_no").val();
    var desc = $("#input_desc").val();
    var example = $("#input_example").val();
    $.ajax({
        url: "/dev/api/add/input/",
        method: "POST",
        data:{desc:desc,api_no:api_no,example:example},
        success:function(data){
            var json_obj = JSON.parse(data);
            if (json_obj.status == true) {
                var new_data = json_obj.data;
                for(var i=0;i<new_data.length;i++) {
                    $("#api_input_exist").append('<div><p>' + new_data[i].desc +'</p><p><textarea class="form-control" readonly>' + new_data[i].example + '</textarea></p></div>');
                }
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

function new_output_example(){
    var api_no = $("#api_no").val();
    var desc = $("#output_desc").val();
    var example = $("#output_example").val();
    $.ajax({
        url: "/dev/api/add/output/",
        method: "POST",
        data:{desc:desc,api_no:api_no,example:example},
        success:function(data){
            var json_obj = JSON.parse(data);
            if (json_obj.status == true) {
                var new_data = json_obj.data;
                for(var i=0;i<new_data.length;i++) {
                    $("#api_output_exist").append('<div><p>' + new_data[i].desc +'</p><p><textarea class="form-control" readonly>' + new_data[i].example + '</textarea></p></div>');
                }
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