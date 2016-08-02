/**
 * Created by msg on 8/1/16.
 */

function Add_Test(api_module_name, api_name, case_name)
{
    var OneTestInfo = "<div>";
    OneTestInfo += '<span class="pull-left text-right width150">API模块：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + api_module_name + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150">API名称：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + api_name + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150">测试名称：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + case_name + '"></input>';
    OneTestInfo += '<span class="clear"></span>';
    OneTestInfo += "</div>";
    $("#div_test_info").append(OneTestInfo);
}

function Add_Test_Info(server_name, api_url, id)
{
    var OneTestInfo = "<div>";
    OneTestInfo += '<span class="pull-left text-right width150">服务环境：</span>';
    OneTestInfo += '<span class="pull-left">' + server_name + '</span>';
    OneTestInfo += '<span class="pull-left text-right width150">请求URL：</span>';
    OneTestInfo += '<span class="pull-left">' + api_url + '</span>';
    OneTestInfo += '<span class="clear"></span>';
    OneTestInfo += '<span class="pull-left text-right width150">测试结果：</span>';
    OneTestInfo += '<span class="pull-left" id="' + id + '">正在测试中</span>';
    OneTestInfo += '<span class="clear"></span>';
    OneTestInfo += "</div>";
    $("#div_test_info").append(OneTestInfo);
}

function Notice_No_Case()
{
    var add_url = location.href.replace("/batch", "");
    var info = "<div>";
    info += "<span>您还没有测试用例</sapn>";
    info += '<a href="' + add_url + '">点击添加</a>';
    $("#div_test_info").append(info);
}

function test_api(){
    if($("#request_url").val() != ""){
        request_url = $("#request_url").val();
    }
    else{
        update_res("无效的请求URL");
        return false;
    }
    var test_case_info = get_param_value();
    if(test_case_info == false){
        return;
    }
    var header_param = test_case_info.header;
    for(var param_key in header_param) {
        var param_value = header_param[param_key];
        if (param_key == "authorization") {
            header_param[param_key] = "Basic " + base64encode(param_value);
        }
        else if (param_key == "X-Authorization") {
            header_param[param_key] = "OAuth2 " + param_value;
        }
        else {
            header_param[param_key] = param_value;
        }
    }
    var body_param = test_case_info.body;
    if(api_method != "GET"){
        body_param = JSON.stringify(body_param)
    }
    $.ajax({
        url: request_url + "?geneacdms=test",
        method: api_method,
        contentType: "application/json",
        headers: header_param,
        //processData: false,
        data: body_param,
        success:function(data){
            console.info(data);
            if(typeof(data) == "string")
            {
                console.info("return json string");
                data = JSON.parse(data);
            }
            update_res(JSON.stringify(data, null, 4));
            update_status_url(data.status);
            $("#btn_save_result").show();
            $("#btn_save_result").text($("#btn_save_result").val());
            $("#save_name").hide();
        },
        error:function(xhr){
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            update_res(res);
            console.info(xhr);
        }
    });
}

var Get_Case_Info_Success = false;
var Get_Case_Info_Data = "";

function get_test_case_success(data){
    Get_Case_Info_Success = data.status;
    Get_Case_Info_Data = data.data;
}

function Write_Result(id, result, status, message)
{
    var status_url = $("#look_status").val();
    if(result == true) {
        status = '<a href="' + status_url + '&status=' + status + '">' + status + '</a>';
        $("#" + id).html("成功" + " 状态码：" + status + " 信息：" + message);
    }
    else
    {
        $("#" + id).html("失败" + " 状态码：" + status + " 信息：" + message);
    }
}

function Run_API(api_url, api_method, case_info, id)
{
    var header_param = new Object();
    for(var param_key in case_info.header) {
        var param_value = case_info.header[param_key];
        if (param_key == "authorization") {
            header_param[param_key] = "Basic " + base64encode(param_value);
        }
        else if (param_key == "X-Authorization") {
            header_param[param_key] = "OAuth2 " + param_value;
        }
        else {
            header_param[param_key] = param_value;
        }
    }
    var body_param = case_info.body;
    if(api_method != "GET"){
        body_param = JSON.stringify(body_param)
    }
    $.ajax({
        url: api_url + "?geneacdms=test",
        method: api_method,
        contentType: "application/json",
        headers: header_param,
        data: body_param,
        success:function(data){
            if(typeof(data) == "string")
            {
                console.info("return json string");
                data = JSON.parse(data);
            }
            Write_Result(id, true, data.status, data.message);
        },
        error:function(xhr){
            Write_Result(id, false, xhr.status, xhr.responseText);
        }
    });
}

function Test_One_API(module_name, api_url, api_title, api_method, test_env, test_case)
{
    var index  = 0;
    for(var i=0;i<test_case.length;i++)
    {
        var case_name = test_case[i];
        Add_Test(module_name, api_title, case_name);
        var test_case_url = $("#test_case_url").val() + case_name + "/";
        my_request(test_case_url, "GET", null, get_test_case_success);
        if(Get_Case_Info_Success == false)
        {
            continue;
        }
        var Url_Param = new Object();
        if("url" in Get_Case_Info_Data){
            Url_Param = Get_Case_Info_Data.url;
        }
        for(var j=0;j<test_env.length;j++){
            var request_url = test_env[j].env_address + api_url;
            for(var key in Url_Param){
                var reg = RegExp("<[^/>]*" + key + ">");
                request_url = request_url.replace(reg, Url_Param[key]);
            }
            var id = "Span_Result_" + index;
            Add_Test_Info(test_env[j].env_name,  request_url, id);
            Run_API(request_url, api_method, Get_Case_Info_Data, id);
            index ++;
        }
    }

}

function get_test_case_list_success(data){
    if(data.status != true){
        update_res(JSON.stringify(data, null, 4));
    }
    if(data.data.length <= 0) {
        Notice_No_Case();
        return;
    }
    var test_envs = $("#test_env option");
    var test_env_info = new Array();
    for(var i=0;i<test_envs.length;i++)
    {
        var env = new Object();
        env["env_name"] = test_envs[i].innerHTML;
        env["env_address"] = test_envs[i].value;
        test_env_info[i] = env;
    }
    Test_One_API($("#module_name").val(), $("#api_url").val(), $("#api_title").val(), $("#api_method").val(), test_env_info, data.data);
}

function get_test_case_list(){
    var test_case_url = $("#test_case_url").val();
    my_async_request(test_case_url, "GET", null, get_test_case_list_success);
}

$(function() {
    get_test_case_list();
});

