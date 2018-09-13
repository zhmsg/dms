/**
 * Created by msg on 12/24/15.
 */
var s_vm = null;
var m_vm = null;
var module_info = new Object();
var error_type = new Object();

var search_type = "in";

function get_module_info_success(data){
    module_info = data.data;
    s_vm.module_info = module_info;
    m_vm.module_info = module_info;
    for(var key in m_vm.module_info){
        m_vm.select_module = key;
        m_vm.change_module();
        break;
    }
    //$("tr[id^='s_']").each(function() {
    //    var code = this.id.substr(2, 8);
    //    var service_id = code.substr(0, 2);
    //    var service_title = module_info[service_id].title;
    //    var fun_id = code.substr(2, 2);
    //    var fun_title = module_info[service_id]["fun_info"][fun_id].title;
    //    $(this).find("td:eq(1)").text(service_title + "-" + fun_title);
    //});
}
function get_module_info() {
    var request_url = $("#fun_info_url").val();
    my_async_request(request_url, "GET", null, get_module_info_success);
}

function get_error_type_success(data){
    error_type = data;
    m_vm.error_type = error_type;
    for(var key in m_vm.error_type){
        m_vm.select_type = key;
        m_vm.update_add_desc();
    }
}
function get_error_type() {
    var request_url = $("#error_type_url").val();
    my_request2(request_url, "GET", null, get_error_type_success);
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
    console.info("enter set fun  id");
    var select_obj = $("#fun_id");
    select_obj.empty();
    var service_id = $("#service_id").val();
    var fun_list = module_info[service_id]["fun_info"];
    for(var key in fun_list){
        add_option("fun_id", key, fun_list[key].title, fun_list[key].title);
    }
    update_info();
}

function set_error_type(){
    var select_obj = $("#type_id");
    select_obj.empty();
    for(var key in error_type){
        add_option("type_id", key, error_type[key].type_title, error_type[key].type_title);
    }
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
    var desc = '<span class="font-red">' + error_type[type_id].type_title + '</span>: '  + error_type[type_id].type_desc;
    $("#error_type_desc").html(desc);
}

function update_info(){
    var service_id = $("#service_id").val();
    var service_text = $("#service_id option:selected").text();
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
    if($("#show_exist").is(':checked')) {
        var code = service_id + fun_id + type_id;
        $("#search_code").val(code);
        search_type = "start";
        filter2(code, "start");
    }
    else{
        search_type = "in";
        filter2($("#search_code").val(), "in");
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


function search_code(){
    var query_s = $("#search_code").val();
    filter2(query_s, search_type);
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


// 显示或隐藏 按钮
$(function(){
    $("#conBtn").click(function(){
        var conBtnValue = $("#conBtn").html();
        if(conBtnValue == "单个新建"){
            set_error_type();
            set_service_id();

            $(".newMode").show();
            $("#conBtn").html("隐藏新建");
            search_type = "start";

            load_location_status();
        }
        if(conBtnValue == "隐藏新建"){
            $(".newMode").hide();
            $("#conBtn").html("单个新建");
            search_type = "in";
        }
    });
});

// 存储当前选中的服务模块与 功能模块
function save_location_status(){
    var current_select = $("#service_id").val() + "," + $("#fun_id").val();
    localStorage.setItem("dms_api_status_add", current_select);
}

function load_location_status(){
    var current_select = localStorage.getItem("dms_api_status_add");
    if(current_select == null){
        return false;
    }
    var select_ids = current_select.split(",");
    if(select_ids.length >= 2) {
        var service_id = select_ids[0];
        var select_options = query_option("service_id", service_id, "value");
        if(select_options.length > 0){
            select_options.attr("selected", true)
        }
        set_fun_id();
        var fun_id = select_ids[1];
        var select_options = query_option("fun_id", fun_id, "value");
        if(select_options.length > 0){
            select_options.attr("selected", true)
        }
        update_info();
    }

}

function filter2(query_s, q_type)
{
    s_vm.show_status = [];
    for(var i=0;i<s_vm.all_status.length;i++){
        if(query_s == null || query_s.length == 0) {
            s_vm.show_status.push(i);
        }
        else{
            var s_item = s_vm.all_status[i];
            if(compare_str(s_item["status_code"], query_s, q_type) || compare_str(s_item["code_desc"], query_s, q_type)){
                s_vm.show_status.push(i);
            }
        }
    }
    s_vm.page_num = Math.ceil(s_vm.show_status.length / s_vm.show_num);

    load_page();
}

function load_page(){
    if(s_vm.current_page <= 0){
        s_vm.current_page = 1;
    }
    if(s_vm.current_page > s_vm.page_num){
        s_vm.current_page = s_vm.page_num;
    }

    s_vm.page_status = [];
    var min_index = (s_vm.current_page - 1) * s_vm.show_num;
    if(min_index < 0){
        min_index = 0;
    }
    var max_index = s_vm.current_page * s_vm.show_num;
    if(max_index >= s_vm.show_status.length){
        max_index = s_vm.show_status.length;
    }
    for(var index=min_index;index<max_index;index++){
        s_vm.page_status.push(s_vm.all_status[s_vm.show_status[index]]);
    }

    var show_page_num = 15;
    var current_page = s_vm.current_page;
    var page_count = s_vm.page_num;
    var start_num = 1;
    var end_num = page_count;
    var mid_num = parseInt((show_page_num + 1) / 2);
    var left_num = show_page_num - mid_num;
    if (current_page <= mid_num) {
        if (page_count > show_page_num) {
            end_num = show_page_num;
        }
    }
    else if (page_count - current_page < left_num) {
        if (page_count > show_page_num) {
            start_num = page_count - show_page_num + 1;
        }
    }
    else {
        start_num = current_page - left_num;
        end_num = start_num + show_page_num - 1;
    }
    s_vm.show_page = [];
    for (var i = start_num; i <= end_num; i++)
    {
        s_vm.show_page.push(i);
    }
}

$(function(){
    s_vm = new Vue({
        el: "#div_list",
        data: {
            all_status: [],  // 所有的状态码
            show_status: [],  // 符合条件的状态码下标
            page_status: [], // 当前页面的状态码
            page_num: 0,
            current_page: 0,
            show_page: [],
            show_num: 15,
            module_info: null
        },
        methods: {
            update_current_page: function(page_num){
                this.current_page = page_num;
                load_page();
            }
        }
    });
    my_request2(location.href, "GET", null, function(data) {
        for (var i = 0; i < data.length; i++) {
            var item = data[i];
            item["code_1"] = item["status_code"].substring(0, 2);
            item["code_2"] = item["status_code"].substring(2, 4);
            item["code_3"] = item["status_code"].substring(4, 6);
            item["code_4"] = item["status_code"].substring(6, 8);
            s_vm.all_status.push(data[i]);

        }
        filter2();
    });
    m_vm = new Vue({
        el: "#div_new_one",
        data: {
            module_info: {},
            select_module: "",
            fun_info: {},
            select_fun: "",
            error_type: {},
            select_type: "",
            add_desc: {"end_code": "00", "desc": ""}
        },
        methods: {
            change_module: function () {
                this.fun_info = this.module_info[this.select_module]["fun_info"];
                for(var key in this.fun_info){
                    this.select_fun = key;
                    break;
                }
                this.update_add_desc();
            },
            update_add_desc: function(){
                this.add_desc["module_title"] = this.module_info[this.select_module]["title"];
                this.add_desc["fun_title"] = this.fun_info[this.select_fun]["title"];
                this.add_desc["type_title"] = this.error_type[this.select_type]["type_title"];
                var end_code = this.add_desc["end_code"];
                if(end_code.length <= 0){
                    end_code = "请填写";
                }
                this.add_desc["end_desc"] = end_code;
                this.add_desc["show_code"] = this.select_module + " " + this.select_fun + " " + this.select_type + " " + end_code;
            }
        }
    });
    get_module_info();
    get_error_type();
    if($("#new_info_show").length > 0){
        $("#service_id").change(set_fun_id);
        $("#fun_id").change(save_location_status);
        $(".updateinfo").change(update_info);
        $("input[id^='error_']").keyup(update_info);
    }
    $("td[name='status_code']").click(function(){
        var current_td = $(this);
        var code = current_td.text().replace(/[^\d]/g, "");
        copy_text(lTrim(code, '0'));
    });
    //鼠标移入显示 移出消失 的效果
    $("tr[id^='s_']").hover(
        function(){
            var code_info = get_info(this.id.substr(2,8));
            $("#status_code_info").html(code_info + "<br /> <p class='redColor'>点击可复制</p>");
            $(".status_out").show();
            $(".status_out").css('top',(this.offsetHeight + this.offsetTop)+'px')
        },
        function(){
            $(".status_out").hide()
        }
    );
});
