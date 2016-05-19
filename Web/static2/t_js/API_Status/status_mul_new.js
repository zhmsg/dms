/**
 * Created by msg on 12/24/15.
 */

var module_info = new Object();
var error_type = new Object();

function my_request(request_url, request_method, body_param, request_success){
    if(request_method != "GET"){
        body_param = JSON.stringify(body_param)
    }
    $.ajax({
        url: request_url,
        method: request_method,
        contentType: "application/json",
        data: body_param,
        success:request_success,
        error:function(xhr){
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            console.info(xhr);
        }
    });
}

function get_module_success(data){
    if (data.status == true){
        module_info = data.data;
        var module_row = new Array();
        var i = 0;
        for(var key in module_info){
            var data = new Array();
            data[0] = key;
            data[1] = module_info[key].title;
            data[2] = module_info[key].desc;
            data[3] = "<a href='#'>删除</a>";
            module_row[i] = data;
            i++;
        }
        add_table_row("tb_main_module", module_row);
        set_service_id();
    }
}

function get_module_info() {
    var request_url = $("#fun_info_url").val();
    console.info(request_url);
    my_request(request_url, "GET", null, get_module_success);
}

function get_error_type_success(data){
    if (data.status == true){
        error_type = data.data;
        var error_row = new Array();
        var i = 0;
        for(var key in error_type)
        {
            var data = new Array();
            data[0] = key;
            data[1] = error_type[key].title;
            data[2] = error_type[key].desc;
            error_row[i] = data;
            i++;
        }
        add_table_row("tb_error_type", error_row, false);
    }
}

function get_error_type() {
    var request_url = $("#error_type_url").val();
    my_request(request_url, "GET", null, get_error_type_success);
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
    var service_id = $("#service_id").val();
    var fun_list = module_info[service_id]["fun_info"];
    var mul_row = new Array();
    var i = 0;
    for(var key in fun_list){
        var row_data = new Array();
        row_data[0] = key;
        row_data[1] = fun_list[key].title;
        row_data[2] = fun_list[key].desc;
        row_data[3] = "<a href='#'>删除</a>";
        mul_row[i] = row_data;
        i++;
    }
    add_table_row("tb_sub_module", mul_row, true);
}

function set_div_show(btn_id, is_show){
    var btn = $("#" + btn_id);
    var btn_v = btn.val();
    var div_class = btn_id.replace("btn", "div");
    if (is_show == true)
    {
        btn.html("隐藏" + btn_v);
        $("." + div_class).show();
    }
    else{
        btn.html(btn_v);
        $("." + div_class).hide();
    }
}
function div_show(btn_id)
{
    var btn = $("#" + btn_id);
    var btn_v = btn.val();
    var btn_html = btn.html();
    if(btn_v == btn_html){
        set_div_show(btn_id, true);
        return true;
    }
    else
    {
        set_div_show(btn_id, false);
        return false;
    }
}

$(function(){
    $("button[id^='btn_new_']").click(function(){
        var id = this.id;
        div_show(id);
        var all_btn = $("button[id^='btn_new_']");
        for(var i=0;i<all_btn.length;i++)
        {
            if(all_btn[i].id == id){
                continue;
            }
            else{
                set_div_show(all_btn[i].id, false)
            }
        }
    });
});


function add_table_row(table_id, mul_row, clear){
    var t = $("#" + table_id);

    if(clear == true){
        t.find("tr:not(:first)").remove();
    }
    var row_len = mul_row.length;
    for(var i=0;i<row_len;i++){
        var row = $("<tr></tr>");
        var row_data = mul_row[i];
        var data_len = row_data.length;
        for(var j=0;j<data_len;j++){
            var td = $("<td></td>");
            td.append(row_data[j]);
            row.append(td);
        }
        t.append(row);
    }

}

$(function(){
    get_module_info();
    get_error_type();
});


function new_module_success(data){
    if(data["status"] == true) {
        var new_data = new Array(new Array(data["data"]["service_id"], data["data"]["service_title"], data["data"]["service_desc"], "<a href='#'>删除</a>"));
        add_table_row("tb_main_module", new_data);
    }
    else{
        alert(data["data"]);
    }
}

function new_sub_module_success(data){
    if(data["status"] == true) {
        var new_data = new Array(new Array(data["data"]["function_id"], data["data"]["function_title"], data["data"]["function_desc"], "<a href='#'>删除</a>"));
        add_table_row("tb_sub_module", new_data);
    }
    else{
        alert(data["data"]);
    }
    alert("success");
}

$(function(){
    $("#new_module").click(function(){
        var id = this.id;
        var module_input = $("input[id^='module_']");
        var body_param = new Object();
        for(var i=0;i<module_input.length;i++){
            body_param[module_input[i].id] = module_input[i].value;
        }
        console.info(body_param);
        var request_url = location.href;
        my_request(request_url, "POST", body_param, new_module_success);
    });
    $("#new_sub_module").click(function(){
        var id = this.id;
        var module_input = $("input[id^='sub_module_']");
        var service_id = $("#service_id").val();
        var body_param = new Object();
        for(var i=0;i<module_input.length;i++){
            body_param[module_input[i].id] = module_input[i].value;
        }
        body_param["service_id"] = service_id;
        console.info(body_param);
        var request_url = $("#fun_info_url").val();
        console.info(request_url);
        my_request(request_url, "POST", body_param, new_sub_module_success);
    });
});