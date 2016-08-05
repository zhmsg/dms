/**
 * Created by msg on 8/1/16.
 */

function Add_Test(api_module_name, api_no, api_name, case_name)
{
    var OneTestInfo = '<div class="top_div">';
    OneTestInfo += '<span class="pull-left text-right width150">API模块：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + api_module_name + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150">API名称：</span>';
    OneTestInfo += '<input class="form-control bug-input" name="api_no" style="display: none" value="' + api_no + '"></input>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + api_name + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150" name="case_name">测试名称：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + case_name + '"></input>';
    OneTestInfo += '<span class="clear"></span>';
    OneTestInfo += "</div>";
    $("#div_test_" + api_no).append(OneTestInfo);
}

function Add_Test_Info(server_name, api_no, api_url, id)
{
    var OneTestInfo = '<div class="bottom_div">';
    OneTestInfo += '<span class="pull-left text-right width150">服务环境：</span>';
    OneTestInfo += '<span name="env_name" class="pull-left">' + server_name + '</span>';
    OneTestInfo += '<span class="pull-left text-right width150">请求URL：</span>';
    OneTestInfo += '<span class="pull-left">' + api_url + '</span>';
    OneTestInfo += '<span class="clear"></span>';
    OneTestInfo += '<span class="pull-left text-right width150">测试结果：</span>';
    OneTestInfo += '<span class="pull-left" id="' + id + '"><span class="error_result">正在测试中</span></span>';
    OneTestInfo += '<span class="clear"></span>';
    OneTestInfo += "</div>";
    $("#div_test_" + api_no).append(OneTestInfo);
}

function Notice_No_Case()
{
    var add_url = location.href.replace("/batch", "");
    var info = "<div>";
    info += "<span>您还没有测试用例</sapn>";
    info += '<a href="' + add_url + '">点击添加</a>';
    $("#div_test_info").append(info);
}


var Get_Case_Info_Success = false;
var Get_Case_Info_Data = "";
var API_Info = new Object();

function get_test_case_success(data){
    Get_Case_Info_Success = data.status;
    Get_Case_Info_Data = data.data;
}

function ReTest(el)
{
    var id = el.parentNode.id;
    var id_info = id.split("_");
    var api_no = id_info[2];
    var case_name = id_info[3];
    var env_name = el.parentNode.parentNode.childNodes[1].innerText;
    var test_url = $("#one_test_url").val() + "?api_no=" + api_no + "&case_name=" + case_name + "&env_name=" + env_name;
    window.open(test_url);
}


function Write_Result(id, result, status, message, expect_status)
{
    var status_url = $("#look_status").val();
    if(result == true) {
        var status_a = '<a href="' + status_url + '&status=' + status + '">' + status + '</a>';
        if(expect_status == status) {
            $("#" + id).html("成功" + " 状态码：" + status_a + " 信息：" + message);
        }
        else{
            $("#" + id).html('<span class="pull-left error_result">失败' + " 状态码：" + status_a + " 信息：" + message + '</span><a href="#">重新测试</a>');
        }
    }
    else
    {
        $("#" + id).html('<span class="pull-left error_result">失败' + " 状态码：" + status + " 信息：" + message + '</span><a href="#" onclick="ReTest(this);">重新测试</a>');
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
    var expect_status = 1000001;
    if("expect_status" in Get_Case_Info_Data){
        expect_status = Get_Case_Info_Data.expect_status;
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

            Write_Result(id, true, data.status, data.message, expect_status);
        },
        error:function(xhr){
            Write_Result(id, false, xhr.status, xhr.statusText);
        }
    });
}

function Test_One_API(api_no, test_env)
{
    var module_name = API_Info[api_no].basic_info.module_name;
    var test_case = API_Info[api_no]["test_case"];
    var api_title = API_Info[api_no].basic_info.api_title;
    var api_method = API_Info[api_no].basic_info.api_method;
    var api_url = API_Info[api_no].basic_info.api_url;
    if(test_case.length <=0){
        Notice_No_Case();
        return;
    }
    var index  = 0;
    for(var i=0;i<test_case.length;i++)
    {
        var case_name = test_case[i];
        Add_Test(module_name, api_no, api_title, case_name);
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
            var id = "Span_Result_" + api_no + "_" + case_name + "_" + index;
            Add_Test_Info(test_env[j].env_name, api_no, request_url, id);
            Run_API(request_url, api_method, Get_Case_Info_Data, id);
            index ++;
        }
    }

}

function get_test_case_list_success(data){
    if(data.status != true){
        update_res(JSON.stringify(data, null, 4));
    }
    var api_no = data.data.api_no;
    API_Info[api_no]["test_case"] = data.data.case;
    console.info(API_Info);
    var test_envs = $("#test_env option");
    var test_env_info = new Array();
    for(var i=0;i<test_envs.length;i++)
    {
        var env = new Object();
        env["env_name"] = test_envs[i].innerHTML;
        env["env_address"] = test_envs[i].value;
        test_env_info[i] = env;
    }
    Test_One_API(api_no, test_env_info);
}

function get_test_case_list(api_no){
    var test_case_url = $("#test_case_url").val() + "?api_no=" + api_no;
    my_async_request(test_case_url, "GET", null, get_test_case_list_success);
}

function Get_API_Info_Success(data) {
    if(data.status == true)
    {
        var api_no = data.data.api_info.basic_info.api_no;
        API_Info[api_no] = data.data.api_info;
        get_test_case_list(api_no);
    }
}

function Get_API_Info(api_no)
{
    var request_url = $("#api_info_url").val() + "?api_no=" + api_no;
    $("#div_test_info").append("<div id='div_test_" + api_no + "'></div>");
    my_async_request(request_url, "GET", null, Get_API_Info_Success);

}

$(function() {
    var api_no = UrlArgsValue(window.location.toString(), "api_no");
    if(api_no != null)
    {
        Get_API_Info(api_no);
    }
});


