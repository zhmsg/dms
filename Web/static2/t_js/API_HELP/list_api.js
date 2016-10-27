/**
 * Created by msg on 3/18/16.
 */


function change_care(module_no){
    if ($("#make_care").text() == "关注")
    {
        new_care(module_no);
    }
    else if($("#make_care").text() == "取消关注")
    {
        remove_care(module_no);
    }
}

function change_care_success(data){
    if (data.status == true){
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
    else{
        sweetAlert(data.data);
    }
}

function new_care(module_no){
    var change_url = $("#care_url").val();
    my_async_request(change_url, "POST", {module_no:module_no}, change_care_success);
}

function remove_care(module_no){
    var change_url = $("#care_url").val();
    my_async_request(change_url, "DELETE", {module_no:module_no}, change_care_success);
}

function add_test_env(){
    var env = $("#s_add_env option:selected");
    var env_no = env.val();
    var env_name = env.text();
    var env_address = env.attr("title");
    var new_span = $("<span></span>");
    new_span.attr("title", env_address);
    new_span.attr("value", env_no);
    new_span.attr("about", env_name);
    new_span.append(env_name);
    new_span.append("<b>X</b>");
    new_span.click(remove_test_env);
    $("#div_add_env").append(new_span);
    env.remove();
}

function remove_test_env(){
    var env_address = this.title;
    var env_name = $(this).attr("about");
    var env_no = $(this).attr("value");
    this.remove();
    add_option("s_add_env", env_no, env_name, env_address);
}


function new_module_success(data){
    if(data.status == true) {
        location.reload();
    }
}

var module_data = null;
var current_module = null;



function Load_API_List(api_list, module_prefix)
{
    var url_prefix = $("#url_prefix").val();
    if(module_prefix[module_prefix.length - 1] == "/"){
        module_prefix = module_prefix.substr(0, module_prefix.length - 1);
    }
    $("#t_api_list tr").not(":first").remove();
    var t = $("#t_api_list");
    for(var i=0;i<api_list.length;i++){
        var api_info = api_list[i];
        var tr_id = 'tr_' + api_info["api_no"];
        var exist_tr = $("#" + tr_id);
        if(exist_tr.length == 1){
            exist_tr.html("");
            var add_tr = exist_tr;
        }
        else {
            var add_tr = $("<tr id='" + tr_id + "'></tr>");
        }
        t.append(add_tr);
        api_info["api_url"] = escape(module_prefix + api_info["api_path"]);
        var keys = ["api_title", "api_url", "api_method", "status"];
        for(var j=0;j<keys.length;j++){
            var key = keys[j];
            add_tr.append(new_td(key, api_info));
        }
        add_tr.append('<td class="text-center"><a href="' + url_prefix + '/info/?api_no=' + api_info["api_no"] + '">查看</a> | <a href="' + url_prefix + '/test/?api_no=' + api_info["api_no"] + '">测试</a></td>');
    }
    console.info("success");
}

function Load_Care_Info(care_info){
    var current_user_name = $("#current_user_name").val();
    $("#module_care_user").empty();
    for(var i=0;i<care_info.length;i++){
        if(care_info[i]["user_name"] == current_user_name){
            $("#module_care_user").append('<span id="mine_care">我</span>');
            $("#make_care").text("取消关注");
        }
        else {
            $("#module_care_user").append('<span>' + care_info[i]["nick_name"] + '</span>');
        }
    }
}

function Get_API_List_Success(data)
{
    if(data.status == true)
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
}

function Get_API_List(module_no)
{
    var request_url = "/dev/api/module/?module_no=" + module_no;
    my_async_request(request_url, "GET", null, Get_API_List_Success);
}

function Load_API_Module(data)
{
    if(data.status == false){
        return false;
    }
    module_data = data.data;
    var url_prefix = $("#url_prefix").val();
    for(var i=0;i<module_data.length;i++){
        var part_info = module_data[i];
        var add_part_div = $('<div class="apiMode api-help-mode"></div>');
        add_part_div.append('<div style="margin-bottom: 10px"><b>【' + part_info["part_desc"] + '】</b><br /></div>');
        for(var j=0;j<part_info["module_list"].length;j++)
        {
            var module_info = part_info["module_list"][j];
            add_part_div.append('<a href="javascript:void(0)" onclick=Get_API_List(' + module_info["module_no"] +')>' + module_info["module_name"] + '</a>');
        }
        $("#div_module_list").append(add_part_div);
        add_option("module_part", part_info["part_no"], part_info["part_name"]);
    }

}

function Load_Test_Env(data){
    if(data.status == true){
        var env_list = data.data;
        for(var i=0;i<env_list.length;i++){
            var one_env = env_list[i];
            add_option("s_add_env", one_env["env_no"], one_env["env_name"], one_env["env_address"]);
        }
    }
}

$(function(){
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
    $("#div_add_env").find("span").click(remove_test_env);

    var current_user_role = parseInt($("#current_user_role").val());
    var role_value = JSON.parse($("#role_value").text());
    if(bit_and(current_user_role, role_value["api_new"])){
        $("div[id^='div_api_new_']").show();
        var test_env_url = $("#test_env_url").val();
        my_async_request(test_env_url, "GET", null, Load_Test_Env)
    }

    var request_url = "/dev/api/module/";
    my_request(request_url, "GET", null, Load_API_Module);
    var module_no = UrlArgsValue(window.location.toString(), "module_no");
    if(module_no != null) {
        var update = UrlArgsValue(window.location.toString(), "update");
        if (update == null) {
            Get_API_List(module_no);
        }
    }

});