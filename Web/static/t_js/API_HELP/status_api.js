/**
 * Created by msg on 12/24/15.
 */

var module_info = new Object();
var error_type = new Object();
function get_module_info() {
    var request_url = $("#fun_info_url").val();
    console.info(request_url);
    $.ajax({
        url: request_url,
        method: "GET",
        success: function (data) {
            if (data.status == true){
                module_info = data.data;
                set_service_id();
            }
        },
        error: function (xhr) {
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            console.info(res);
        }
    });
}
function get_error_type() {
    var request_url = $("#error_type_url").val();
    console.info(request_url);
    $.ajax({
        url: request_url,
        method: "GET",
        success: function (data) {
            if (data.status == true){
                error_type = data.data;
                set_error_type();
            }
        },
        error: function (xhr) {
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            console.info(res);
        }
    });
}
function add_option(select_obj, value, text){
    var option = "<option value='{value}'>{text}</option>";
    var option_item = option.replace("{value}", value).replace("{text}", text);
    select_obj.append(option_item);
}
function set_service_id(){
    var select_obj = $("#service_id");
    select_obj.empty();
    for(var key in module_info){
        add_option(select_obj, key, module_info[key].title);
    }
    set_fun_id();
}
function set_fun_id(){
    var select_obj = $("#fun_id");
    select_obj.empty();
    var service_id = $("#service_id").val();
    var fun_list = module_info[service_id]["fun_info"];
    for(var key in fun_list){
        add_option(select_obj, key, fun_list[key].title);
    }
    update_info();
}

function set_error_type(){
    var select_obj = $("#type_id");
    select_obj.empty();
    for(var key in error_type){
        add_option(select_obj, key, error_type[key].title);
    }
    update_info();
}
function update_info(){
    var service_id = $("#service_id").val();
    var service_text = $("#service_id  option:selected").text();
    var fun_id = $("#fun_id").val();
    var fun_text = $("#fun_id  option:selected").text();
    var type_id = $("#type_id").val();
    var type_text = $("#type_id  option:selected").text();
    var info = "您将新建一个服务模块为 " + service_text;
    info += " 功能模块为 " + fun_text;
    info += " 错误类型为 " + type_text;
    info += " 错误状态码为 " + $("#error_id").val();
    info += " 错误描述为 " + $("#error_desc").val();
    info += " 最终状态码为 " + service_id + " " + fun_id + " " + type_id + " " + $("#error_id").val();
    $("#new_info_show").text(info);
}
get_module_info();
get_error_type();