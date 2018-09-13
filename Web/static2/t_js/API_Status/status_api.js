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
    if(!(m_vm.select_module in m_vm.module_info)) {
        for (var key in m_vm.module_info) {
            m_vm.select_module = key;
            break;
        }
    }
    m_vm.change_module();
}
function get_module_info() {
    var request_url = $("#fun_info_url").val();
    my_async_request(request_url, "GET", null, get_module_info_success);
}

function get_error_type_success(data){
    error_type = data;
    m_vm.error_type = error_type;
    if(!(m_vm.select_type in m_vm.error_type)) {
        for (var key in m_vm.error_type) {
            m_vm.select_type = key;
        }
    }
    m_vm.update_add_desc();
}
function get_error_type() {
    var request_url = $("#error_type_url").val();
    my_request2(request_url, "GET", null, get_error_type_success);
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
            $(".newMode").show();
            $("#conBtn").html("隐藏新建");
            search_type = "start";
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
    var current_select = m_vm.select_module + "," + m_vm.select_fun + "," + m_vm.select_type;
    localStorage.setItem("dms_api_status_add", current_select);
}

function load_location_status(){
    var current_select = localStorage.getItem("dms_api_status_add");
    console.info(current_select);
    if(current_select == null){
        return false;
    }
    var select_ids = current_select.split(",");
    if(select_ids.length >= 2) {
        m_vm.select_module = select_ids[0];
        m_vm.select_fun = select_ids[1];
        if(select_ids.length >= 3){
            m_vm.select_type = select_ids[2];
        }
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
            },
            copy_code: function(code){
                copy_text(lTrim(code, '0'));
            },
            delete_code: function(code){
                var delete_url = $("#url_code").val();
                my_async_request2(delete_url, "DELETE", {"status_code": code}, function(data){
                    var index = -1;
                    for(var i=s_vm.all_status.length - 1;i>=0;i--){
                        if(s_vm.all_status[i]["status_code"] == data){
                            index = i;
                            s_vm.all_status.splice(index, 1);
                        }
                    }
                    if(index == -1){
                        return false;
                    }
                    search_code();
                });

            }
        }
    });
    my_request2($("#url_code").val(), "GET", null, function(data) {
        for (var i = 0; i < data.length; i++) {
            var item = data[i];
            item["code_1"] = item["status_code"].substring(0, 2);
            item["code_2"] = item["status_code"].substring(2, 4);
            item["code_3"] = item["status_code"].substring(4, 6);
            item["code_4"] = item["status_code"].substring(6, 8);
            s_vm.all_status.push(data[i]);

        }
        search_code();
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
            add_desc: {},
            status_end_code: "",
            status_code_desc: "",
            filter_similar_code: false
        },
        methods: {
            change_module: function () {
                this.fun_info = this.module_info[this.select_module]["fun_info"];
                if(!( this.select_fun in this.fun_info)) {
                    for (var key in this.fun_info) {
                        this.select_fun = key;
                        break;
                    }
                }
                this.update_add_desc();
                save_location_status();
            },
            change_fun: function(){
                this.update_add_desc();
                save_location_status();
            },
            change_type: function(){
                this.update_add_desc();
                save_location_status();
            },
            update_add_desc: function(){
                this.add_desc["module_title"] = this.module_info[this.select_module]["title"];
                this.add_desc["module_desc"] = this.module_info[this.select_module]["desc"];
                this.add_desc["fun_title"] = this.fun_info[this.select_fun]["title"];
                this.add_desc["fun_desc"] = this.fun_info[this.select_fun]["desc"];
                this.add_desc["type_title"] = this.error_type[this.select_type]["type_title"];
                this.add_desc["type_desc"] = this.error_type[this.select_type]["type_desc"];
                var end_code = this.status_end_code;
                if(end_code.length <= 0){
                    end_code = "请填写";
                }
                this.add_desc["show_code"] = this.select_module + " " + this.select_fun + " " + this.select_type + " " + end_code;
                if(this.filter_similar_code == true){
                    var code_prefix =  this.select_module + this.select_fun + this.select_type;
                    filter2(code_prefix, "start");
                }
            },
            add_action: function(){
                var data = {"service_id": this.select_module, "fun_id": this.select_fun, "type_id": this.select_type};
                if(this.status_end_code.length <= 0){
                    alert1("请填写末位状态码");
                    return false;
                }
                if(this.status_code_desc.length <= 0){
                    alert1("请填写状态解释");
                    return false;
                }
                data["error_id"] = this.status_end_code;
                data["error_desc"] = this.status_code_desc;
                console.info(data);
                my_async_request2($("#url_code").val(), "POST", data);
            }
        },
        watch: {
            status_end_code: function(){
                this.update_add_desc();
            },
            filter_similar_code: function(val){
                if(val == true){
                    var code_prefix =  this.select_module + this.select_fun + this.select_type;
                    filter2(code_prefix, "start");
                }
                else{
                    filter2();
                }
            }
        }
    });
    load_location_status();
    get_module_info();
    get_error_type();

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
