/**
 * Created by msg on 8/1/16.
 */

var API_Info = new Object();
var Env_Info = new Object();

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
    if("expect_status" in case_info){
        expect_status = case_info.expect_status;
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

function Get_Case_Info_Success(data){
    if(data.status == false)
    {
        return;
    }
    var case_info = data.data;
    var case_name = case_info.case_name;
    var api_no = case_info.api_no;
    var api_method = API_Info[api_no].basic_info.api_method;
    var api_url = API_Info[api_no].basic_info.api_url;
    var Url_Param = new Object();
    if("url" in case_info){
        Url_Param = case_info.url;
    }
    var index = 0;
    var test_env_info = API_Info[api_no]["env_info"];
    for(var j=0;j<test_env_info.length;j++){
        var request_url = test_env_info[j].env_address + api_url;
        for(var key in Url_Param){
            var reg = RegExp("<[^/>]*" + key + ">");
            request_url = request_url.replace(reg, Url_Param[key]);
        }
        var id = "Span_Result_" + api_no + "_" + case_name + "_" + index;
        Add_Test_Info(test_env_info[j].env_name, api_no, case_name, request_url, id);
        Run_API(request_url, api_method, case_info, id);
        index ++;
    }
}

function Test_One_API(api_no)
{
    var module_name = API_Info[api_no].basic_info.module_name;
    var test_case = API_Info[api_no]["test_case"];
    var api_title = API_Info[api_no].basic_info.api_title;
    if(test_case.length <=0){
        Notice_No_Case(api_no);
        return;
    }
    for(var i=0;i<test_case.length;i++)
    {
        var case_name = test_case[i];
        Add_Test(module_name, api_no, api_title, case_name);
        var test_case_url = $("#test_case_url").val() + case_name + "/?api_no=" + api_no;
        my_async_request(test_case_url, "GET", null, Get_Case_Info_Success);
    }

}

function Get_Case_List_Success(data){
    if(data.status != true){
        update_res(JSON.stringify(data, null, 4));
    }
    var api_no = data.data.api_no;
    API_Info[api_no]["test_case"] = data.data.case;
    Test_One_API(api_no);
}

function Get_API_Info_Success(data) {
    if(data.status == true)
    {
        var api_no = data.data.api_info.basic_info.api_no;
        var env_str = data.data.api_info.basic_info.module_env;
        var env_sp = env_str.split("|");
        API_Info[api_no] = data.data.api_info;
        API_Info[api_no]["env_info"] = new Array();
        var i = 0;
        for(var index in env_sp)
        {
            if(env_sp[index] in Env_Info){
                API_Info[api_no]["env_info"][i] = Env_Info[env_sp[index]];
                i++;
            }
        }
        console.info(API_Info[api_no]);
        var test_case_url = $("#test_case_url").val() + "?api_no=" + api_no;
        my_async_request(test_case_url, "GET", null, Get_Case_List_Success);
    }
}

function Get_API_Info(api_no)
{
    var request_url = $("#api_info_url").val() + "?api_no=" + api_no;
    $("#div_test_info").append("<div id='div_" + api_no + "'></div>");
    my_async_request(request_url, "GET", null, Get_API_Info_Success);

}

function Get_Env_Info_Success(data)
{
    if(data.status == true)
    {
        for(var i=0;i<data.data.length;i++)
        {
            Env_Info["" + data.data[i].env_no] = data.data[i];
        }
    }
}

function Get_Env_Info()
{
    var request_url = $("#env_info_url").val();
    my_request(request_url, "GET", null, Get_Env_Info_Success)
}

function Get_API_List_Success(data)
{
    if(data.status == true)
    {
        var api_list = data.data.api_list;
        for(var i=0;i<api_list.length;i++){
            Get_API_Info(api_list[i].api_no);
        }
    }
}

function Get_API_List(module_no)
{
    var request_url = $("#module_api_url").val() + "?module_no=" + module_no;
    my_async_request(request_url, "GET", null, Get_API_List_Success);
}

$(function() {
    Get_Env_Info();
    var module_no = UrlArgsValue(window.location.toString(), "module_no");
    if(module_no != null){
        Get_API_List(module_no);
    }
    else {
        var api_no = UrlArgsValue(window.location.toString(), "api_no");
        if (api_no != null) {
            Get_API_Info(api_no);
        }
    }
});


