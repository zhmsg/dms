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
            alert(data);
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
            alert(data);
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
            alert(data);
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
            alert(data);
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}