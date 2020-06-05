/**
 * Created by msg on 12/24/15.
 */

var module_info = new Object();
var error_type = new Object();

function get_module_success(data){
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

function get_module_info() {
    var request_url = $("#fun_info_url").val();
    console.info(request_url);
    my_request(request_url, "GET", null, get_module_success);
}

function new_checkbox(id, chang_func, lab_text){
    var lab = $('<label class="checkbox-inline"></label');
    var cb = $("<input type='checkbox' id='"+ id + "' onchange='" + chang_func + "();' checked>");
    lab.append(cb);
    lab.append(lab_text);
    return lab;
}

function get_error_type_success(data){
    error_type = data.data;
    var error_row = new Array();
    var i = 0;
    for(var key in error_type)
    {

        var data = new Array();
        data[0] = key;
        data[1] = error_type[key].type_title;
        data[2] = error_type[key].desc;
        error_row[i] = data;
        i++;
        if(error_type[key].type_title.indexOf("参数") >= 0) {
            var new_cb = new_checkbox("error_type_" + key, "preview_status_code", error_type[key].type_title);
            $("#p_status_prefix").append(new_cb);
        }
    }
    add_table_row("tb_error_type", error_row, false);
}

function get_error_type() {
    var request_url = $("#error_type_url").val();
    my_request(request_url, "GET", null, get_error_type_success);
}


function set_service_id(){
    var select_obj = $("#service_id");
    select_obj.empty();
    for(var key in module_info){
        add_option("service_id", key, module_info[key].title, module_info[key].title);
    }
    set_fun_id();
}


function set_fun_id(){
    var select_obj = $("#fun_id");
    select_obj.empty();
    var service_id = $("#service_id").val();
    var fun_list = module_info[service_id]["fun_info"];
    for(var key in fun_list){
        add_option("fun_id", key, fun_list[key].title, fun_list[key].title);
    }
    preview_status_code();
}

function preview_status_code(){
    var service_id = $("#service_id").val();
    var fun_id = $("#fun_id").val();
    var param_name = $("#param_name").val();
    if(param_name == ""){
        param_name = "<b>【请输入参数名】</b>";
    }
    var param_type = $("#param_type").val();
    var new_status_code = new Array();
    var prefix_code = service_id+ " " + fun_id;
    var select_cb = $("input:checkbox[id^='error_type_']:checked");
    for(var i=0;i<select_cb.length;i++){
        var error_type_key = select_cb[i].id.substr(11, 2);
        var status_code_desc = "";
        if(error_type_key == "01"){
            status_code_desc += "需要参数" + param_name + "，在请求中未发现此参数";
        }
        else if(error_type_key == "02")
        {
            status_code_desc += param_name + "类型不正确，应该为" + param_type + "类型";
        }
        else if(error_type_key == "03")
        {
            status_code_desc += "提供的" + param_name + "不合法，可能包含非法字符或者长度不符合基本要求";
        }
        else if(error_type_key == "04")
        {
            status_code_desc += "提供的" + param_name + "，经服务器验证后判定为无效";
        }
        new_status_code[i] = new Array(prefix_code + " " + error_type_key + " **", status_code_desc, "");
    }
    add_table_row("tb_preview_code", new_status_code, true);
}

function del_status_code_success(data){
    $("#a_del_" + data.data).parent().parent().remove();
}

function new_mul_status_code_success(data){
    var t_name = "tb_preview_code";
    clear_table(t_name);
    var keys = ["status_code", "error_desc"];
    for(var i=0;i<data.data.length;i++){
        var add_tr = $("<tr></tr>");
        for (var j = 0; j < keys.length; j++) {
            add_tr.append(new_td(keys[j], data.data[i]));
        }
        var del_code_a = '<a id="a_del_' + data.data[i].status_code + '" href="javascript:void(0)" title="">删除</a>';
        //add_rows[i] = new Array(data.data[i].status_code, data.data[i].error_desc, del_code_a);
        var add_td = $("<td>" + del_code_a + "</td>");
        add_tr.append(add_td);
        $("#" + t_name).append(add_tr);
    }
    //add_table_row("tb_preview_code", add_rows, true);
    $("a[id^=a_del_]").click(function(){
        var status_code = this.id.substring(6);
        var del_url = $("#del_status_code_url").val();
        var body_param = new Object();
        body_param["status_code"] = status_code;
        my_request(del_url, "DELETE", body_param, del_status_code_success);
    });
    $("td[name='td_status_code']").each(function () {
        var current_td = $(this);
        current_td.addClass("status_move");
        current_td.click(function () {
            var code = current_td.text().replace(/[^\d]/g, "");
            copy_text(lTrim(code, '0'));
        });

    });
}

function new_mul_status_code()
{
    var service_id = $("#service_id").val();
    var fun_id = $("#fun_id").val();
    var param_name = $("#param_name").val();
    if(param_name == ""){
        alert("【请输入参数名】");
        return;
    }
    t = $("#tb_preview_code");
    var tr_status = t.find("tr:not(:first)");
    var body_param = new Object();
    body_param["service_id"] = service_id;
    body_param["fun_id"] = fun_id;
    body_param["error_info"] = new Array();
    for(var i=0;i<tr_status.length;i++){
        var code = tr_status[i].cells[0].innerHTML;
        var type_id = code.substr(6, 2);
        var desc = tr_status[i].cells[1].innerHTML;
        body_param["error_info"][i] = new Object();
        body_param["error_info"][i]["type_id"] = parseInt(type_id);
        body_param["error_info"][i]["error_desc"]= desc;
    }
    console.info(body_param);
    my_request(location.href, "POST", body_param, new_mul_status_code_success);
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

$(function(){
    $("#btn_param_mul").click(new_mul_status_code);
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
    get_error_type();
    get_module_info();
});
