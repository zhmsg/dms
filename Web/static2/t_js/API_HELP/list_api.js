/**
 * Created by msg on 3/18/16.
 */

var m_vm = null;
var api_vm = null;
var env_vm = null;

function change_care() {
    if ($("#make_care").text() == "关注")
    {
        new_care();
    }
    else if($("#make_care").text() == "取消关注")
    {
        remove_care();
    }
}

function change_care_success(data){
    if ($("#make_care").text() == "关注")
    {
        $("#make_care").text("取消关注");
        $("#module_care_user").append('<span id="mine_care">我</span>');
    }
    else if($("#make_care").text() == "取消关注")
    {
        $("#make_care").text("关注");
        $("#mine_care").remove();
    }
}

function new_care() {
    var change_url = $("#care_url").val();
    my_async_request(change_url, "POST", null, change_care_success);
}

function remove_care() {
    var change_url = $("#care_url").val();
    my_async_request(change_url, "DELETE", null, change_care_success);
}


function new_module_success(data){
    location.reload();
}

var module_data = null;
var current_module = null;


function Get_API_List_Success(data)
{
    $("#div_api_list").show();
    $("#div_api_new_add").hide();
    var module_no = data.data.module_info.module_no;
    for(var i=0;i<module_data.length;i++){
        var part_info = module_data[i];
        for(var j=0;j<part_info["module_list"].length;j++)
        {
            if(module_no == part_info["module_list"][j]["module_no"])
            {
                current_module = part_info["module_list"][j]
            }
        }
    }
    if(current_module == null){
        return false;
    }
    Load_Module_Info("info");
    var api_list = data.data.api_list;
    var module_prefix = current_module["module_prefix"];
    Load_API_List(api_list, module_prefix);
    var care_info = data.data.care_info;
    Load_Care_Info(care_info);
    $("#a_add_api").attr("href", $("#a_add_api").attr("href_prefix") + module_no);
    $("#a_del_module").attr("href", $("#a_del_module").attr("href_prefix") + module_no);
    $("#a_test_module").attr("href", $("#a_test_module").attr("href_prefix") + module_no);
}

function Get_API_List(module_no)
{
    $("a[id^='a_module_']").removeClass();
    $("#a_module_" + module_no).addClass("selected");
    var request_url = $("#module_url").val() + "?module_no=" + module_no;
    my_async_request(request_url, "GET", null, Get_API_List_Success);
}


$(function(){
    var url_prefix = $("#url_prefix").val();
    m_vm = new Vue({
        el: "#div_module_list",
        data: {
            url_prefix: url_prefix,
            modules_data: []
        },
        methods: {
            to_module: function(module_no){
                var url = url_prefix + '/?module_no=' + module_no;
                location.href = url;
            }
        }
    });
    api_vm = new Vue({
        el: "#t_api_list",
        data: {
            url_prefix: url_prefix,
            api_list: []
        },
        methods: {
            to_copy: function(content){
                copy_text(content);
            }
        }
    });

    env_vm = new Vue({
        el: "#li_test_env",
        data: {
            all_env: [],
            selected_index: 0,
            use_env: []
        },
        methods: {
            select: function(){
                this.all_env[this.selected_index].selected = true;
                for(var i=0;i<this.all_env.length;i++){
                    if(this.all_env[i].selected==false){
                        this.selected_index = i;
                        break;
                    }
                }
            },
            cancel_select: function(index){
                this.all_env[index].selected = false;
                this.selected_index = index;
            }
        }
    });

    $("#btn_op_module").click(function(){
        var body_param = new Object();
        var method = "POST";
        if(current_module != null) {
            body_param["module_no"] = current_module["module_no"];
            method = "PUT";
        }
        body_param["module_name"] = $("#module_name").val();
        body_param["module_prefix"] = $("#module_prefix").val();
        body_param["module_desc"] = $("#module_desc").val();
        body_param["module_part"] = parseInt($("#module_part").val());
        body_param["module_env"] = new Array();
        var all_span_env = $("#div_add_env").find("span");
        var span_len = all_span_env.length;
        for(var i=0;i<span_len;i++) {
            body_param["module_env"][i] = parseInt($(all_span_env[i]).attr("value"));
        }
        var request_url = $("#module_url").val();
        my_request(request_url, method, body_param, new_module_success);
    });


    var current_user_role = parseInt($("#current_user_role").val());
    var role_value = JSON.parse($("#role_value").text());
    if(bit_and(current_user_role, role_value["api_new"])){
        $("div[id^='div_api_new_']").show();
        var test_env_url = $("#test_env_url").val();
        my_async_request2(test_env_url, "GET", null, function (data) {
            for(var i=0;i<data.length;i++){
                data[i].selected = false;
                env_vm.all_env.push(data[i]);
            }
        });
    }

    var request_url = $("#module_url").val();
    my_request(request_url, "GET", null, Load_API_Module);
    var module_no = UrlArgsValue(window.location.toString(), "module_no");
    if(module_no != null) {
        var update = UrlArgsValue(window.location.toString(), "update");
        if (update == null) {
            Get_API_List(module_no);
        }
    }
    $("#a_query_list").click(function(){
        var current_stage = $("#a_query_list").text();
        if(current_stage == "搜索列表"){
            $("#a_query_list").text("隐藏搜索");
            $("#search_api_list").show();
            $("#search_api_list").keyup(function(){
                var query_key = $("#search_api_list").val();
                query_table("t_api_list", query_key);
            });
        }
        else{
            $("#a_query_list").text("搜索列表");
            $("#search_api_list").hide();
            $("#search_api_list").unbind('keyup');
            $("#search_api_list").val("");
            query_table("t_api_list", "");
        }
    });

});