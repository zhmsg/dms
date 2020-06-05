/**
 * Created by msg on 12/24/15.
 */

var module_info = new Object();
var error_type = new Object();


function get_module_info_success(data){
    module_info = data.data;
}
function get_module_info() {
    var request_url = $("#fun_info_url").val();
    my_async_request(request_url, "GET", null, get_module_info_success);
}

function get_error_type_success(data){
    error_type = data.data;
}
function get_error_type() {
    var request_url = $("#error_type_url").val();
    my_async_request(request_url, "GET", null, get_error_type_success);
}


function load_status(data)
{
    var l = data.items.length;
    if(l > 0){
        var item = data.items[0];
        var code = item.status_code;
        $("#r_status_code").text(code);
        $("#r_code_desc").text(item.code_desc);
        var service_id = code.substr(0, 2);
        var service = module_info[service_id];
        var fun_id = code.substr(2, 2);
        var fun = module_info[service_id]["fun_info"][fun_id];
        var et = error_type[code.substr(4, 2)];
        $("#r_service").text(service.title);
        $("#r_service").attr("title", service.desc);
        $("#r_module").text(fun.title);
        $("#r_module").attr("title", fun.desc);
        $("#r_type").text(et.title);
        $("#r_type").attr("title", et.desc);
        $("#t_show").show();
        $("#t_not_found").hide();
    }
    else{
        $("#td_not_found").text("没有搜到 " + data.q);
        $("#t_show").hide();
        $("#t_not_found").show();
    }
}

$(function(){
    $('#search_code').keydown(function(e){
        if(e.keyCode==13){
            console.info("start search");
            var code = $('#search_code').val();
            if(code.length > 0){
                console.info(code);
                my_async_request2(location.href, "GET", {"status": code}, load_status);
            }
        }
    });
    get_module_info();
    get_error_type();
});
