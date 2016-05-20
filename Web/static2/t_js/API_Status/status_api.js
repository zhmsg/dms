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

function fun_update(){
    var service_id = $("#service_id").val();
    var fun_id = $("#fun_id").val();
    var service_desc = '<span class="font-red">' + module_info[service_id].title + '</span>: '  + module_info[service_id].desc;
    var fun_desc = '<span class="font-red">' + module_info[service_id]["fun_info"][fun_id].title + '</span>: '  + module_info[service_id]["fun_info"][fun_id].desc;
    $("#service_desc").html(service_desc);
    $("#fun_desc").html(fun_desc);
}
function error_type_update(){
    var type_id = $("#type_id").val();
    var desc = '<span class="font-red">' + error_type[type_id].title + '</span>: '  + error_type[type_id].desc;
    $("#error_type_desc").html(desc);
}

function update_info(){
    var service_id = $("#service_id").val();
    var service_text = $("#service_id  option:selected").text();
    var fun_id = $("#fun_id").val();
    var fun_text = $("#fun_id  option:selected").text();
    var type_id = $("#type_id").val();
    var type_text = $("#type_id  option:selected").text();
    var info = "您将新建一个服务模块为 " + '<span class="font-red">' + service_text + '</span>';
    info += " 功能模块为 " + '<span class="font-red">' + fun_text + '</span>';
    info += " 错误类型为 " + '<span class="font-red">' + type_text + '</span>';
    var error_id = $("#error_id").val();
    var invalid_input = false;
    if(error_id.length <= 0){
        error_id = "请填写";
        invalid_input = true;
    }
    else {
        var error_id_int = parseInt(error_id);
        if (isNaN(error_id_int)) {
            error_id = "必须为正整数";
            invalid_input = true;
        }
        else if (error_id_int < 0 || error_id_int >= 100) {
            error_id = "必须小于100";
            invalid_input = true;
        }
    }
    info += " 错误状态码为 " + '<span class="font-red">' + error_id + '</span>';
    var error_desc = $("#error_desc").val();
    if (error_desc.length <= 0){
        error_desc = "请填写";
        invalid_input = true;
    }
    if(invalid_input == true){
        $("#btn_new").attr({"disabled":"disabled"});
    }
    else{
        $("#btn_new").removeAttr("disabled");
    }
    //$("#btn_new").disabled = invalid_input;
    info += " 错误描述为 " + '<span class="font-red">' + error_desc + '</span>';
    info += " 最终状态码为 " + '<span class="font-red">' + service_id + " " + fun_id + " " + type_id + " " + error_id + '</span>';
    $("#new_info_show").html(info);
    fun_update();
    error_type_update();
    console.info($("#show_exist").attr("checked"));
    if($("#show_exist").is(':checked')) {
        filter_code(service_id + fun_id + type_id, "start", 1);
    }
    else{
        filter_code($("#search_code").val(), "in", 1);
    }
}


function compare_str(l_s, s_s, c_type){
    if(c_type == "in"){
        if(l_s.indexOf(s_s) >= 0) {
            return true
        }
    }
    else if(c_type == "start"){
        if(l_s.indexOf(s_s) == 0) {
            return true
        }
    }
    return false
}

function filter_code(code, s_type, page_num){
    var trs = $("tr[id^='s_']");
    var tr_len = trs.length;
    var match_count = 0;
    var show_count = 15;
    var start_num = (page_num - 1) * show_count;
    var end_num = start_num + show_count;
    var i = 0;
    for(; i < tr_len; i++){
        var tr = trs[i];
        if(compare_str(tr.id.substr(2, 8), code, s_type) == true){
            match_count++;
            if(match_count <= start_num || match_count > end_num) {
                tr.hidden = true;
            }
            else {
                tr.hidden = false;
            }
        }
        else{
            tr.hidden = true;
        }
    }
    add_page_num((match_count - 1 ) / show_count + 1);
}

function search_code(page_num){
    var query_s = $("#search_code").val();
    filter_code(query_s, "in", page_num);
}

function get_info(code){
    var service_id = code.substr(0, 2);
    var service_title = module_info[service_id].title;
    var fun_id = code.substr(2, 2);
    var fun_title = module_info[service_id]["fun_info"][fun_id].title;
    var type_id = code.substr(4, 2);
    var type_title = error_type[type_id].title;
    var info = service_title + "<br />" + fun_title + "<br />" + type_title;
    return info;
}

$(function(){
    //鼠标移入显示 移出消失 的效果
    $("tr[id^='s_']").hover(
        function(){
            var code_info = get_info(this.id.substr(2,8));
            $("#status_code_info").html(code_info);
            $(".status_out").show();
            $(".status_out").css('top',(this.offsetHeight + this.offsetTop)+'px')
        },
        function(){
            $(".status_out").hide()
        }
    );
});

// 显示或隐藏 按钮
$(function(){
    $("#conBtn").click(function(){
        var conBtnValue = $("#conBtn").html();
        if(conBtnValue == "单个新建"){
            $(".newMode").show();
            $("#conBtn").html("隐藏新建");
        }
        if(conBtnValue == "隐藏新建"){
            $(".newMode").hide();
            $("#conBtn").html("单个新建");
        }
    });
});

$(function(){
    get_module_info();
    get_error_type();
});

// 分页相关方法
function add_page_num(num){
    var u = $("#pagination");
    u.find("li").remove();
    for(var i=1;i<=num;i++){
        u.append('<li id=li_page_' + i + '><a href="#">' + i + '</a></li>');
    }
    $("li[id^='li_page_']").click(function(){
        var page_num = parseInt(this.id.substr(8));
        search_code(page_num);
    });
}