/**
 * Created by msg on 8/4/16.
 */

function test_api(){
    update_res("正在请求...");
    $("#btn_save_result").hide();
    $("#btn_save_output").hide();
    var test_env = $("#test_env").val();
    var api_url = $("#api_url").val();
    var api_method = $("#api_method").val();
    var request_url = test_env + api_url;
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
    var python_cmd = "";
    python_cmd += "import requests\n";
    var cmd_request_options = new Array();
    var cmd_request_headers = new Object();
    var cmd_request_data = new Object();
    var header_param = test_case_info.header;
    for(var param_key in header_param) {
        var param_value = header_param[param_key];
        if (param_key == "authorization") {
            if($("#skip_auth").is(':checked')){
                header_param["X-Skip-Auth"] = param_value.split(":")[0];
                cmd_request_headers["X-Skip-Auth"] = header_param["X-Skip-Auth"];

            }
            else {
                var auth_split = param_value.split(":");
                if(auth_split.length != 2){
                    update_res("请输入正确的authorization,例如zh_test:123456");
                    return false;
                }
                header_param[param_key] = "Basic " + base64encode(param_value);
                cmd_request_options[cmd_request_options.length] = "auth=(\"" + auth_split.join("\", \"") + "\")";
            }
        }
        else if (param_key == "X-Authorization") {
            header_param[param_key] = "OAuth2 " + param_value;
            cmd_request_headers[param_key] = header_param[param_key];
        }
        else {
            header_param[param_key] = param_value;
            cmd_request_headers[param_key] = header_param[param_key];
        }
    }
    var body_param = test_case_info.body;
    if(api_method != "GET"){
        python_cmd += "request_args = dict()\n";
        for(var key in body_param){
            python_cmd += "request_args[\"" + key + "\"] = \"" + body_param[key] + "\"";
        }
        body_param = JSON.stringify(body_param);
    }

    python_cmd += "response = requests.request()";
    console.info(python_cmd);
    console.info(cmd_request_options);
    $.ajax({
        url: request_url + "?geneacdms=test",
        method: api_method,
        contentType: "application/json",
        headers: header_param,
        data: body_param,
        success:function(data){
            if(typeof(data) == "string")
            {
                data = JSON.parse(data);
            }
            update_res(JSON.stringify(data, null, 4));
            $("#expect_status").val(data.status);
            update_status_url(data.status);
            $("#btn_save_result").show();
            if(new_right == true) {
                $("#btn_save_output").show();
            }
            $("#btn_save_result").text($("#btn_save_result").val());
            $("#save_name").hide();
        },
        error:function(xhr){
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            update_res(res);
        }
    });
}


function save_test_case(){
    var case_name = $("#test_case_name").val();
    var expect_status = $("#expect_status").val();
    var test_case_info = get_param_value();
    if(test_case_info == false) {
        return;
    }
    var test_case_url = $("#test_case_url").val();
    test_case_info["case_name"] = case_name;
    test_case_info["expect_status"] = parseInt(expect_status);
    my_async_request(test_case_url, "POST", test_case_info);
    add_case_node(case_name);
}

function save_output_example(){
    var request_url = $("#api_example_url").val();
    var output_desc = $("#output_desc").val();
    var output_example = $("#res_text").val();
    my_async_request(request_url, "POST", {"desc": output_desc, "content": output_example, "example_type": 2}, null);
}

function get_test_case_success(data){
    $("input[id$='_value']").val("");
    var case_info = data.data;
    if("header" in case_info){
        for(var key in case_info.header){
            var v = case_info.header[key];
            $("#" + key + "_value").val(v);
        }
    }
    if("body" in case_info){
        for(var key in case_info.body){
            var v = case_info.body[key];
            if(v instanceof  Array) {
                v = JSON.stringify(v);
                $("#" + key + "_type").val("list");
            }
            else if(v instanceof Object) {
                v = JSON.stringify(v);
                $("#" + key + "_type").val("object");
            }
            else if(typeof v == "number"){
                $("#" + key + "_type").val("int");
            }
            else if(typeof v == "boolean"){
                $("#" + key + "_type").val("bool");
            }
            else{
                $("#" + key + "_type").val("string");
            }
            $("#" + key + "_value").val(v);
        }
    }
    if("url" in case_info){
        for(var key in case_info.url){
            $("#url_value_" + key).val(case_info.url[key]);
        }
    }
    if("expect_status" in case_info){
        $("#expect_status").val(case_info.expect_status);
    }
    update_request_url();
    update_res("加载保存的测试用例 " + case_info.case_name + " 成功");
    $("#test_case_name").val(case_info.case_name);
}

function add_case_node(case_name)
{
    var div_test_case = $("#div_test_case");
    var id = "a_case_" + case_name;
    if($("#" + id).length > 0){
        return;
    }
    div_test_case.append('<a href="javascript:void(0)" id="' + id + '" class="test_case margin10">' + case_name + '</a>');
    $("a[id='"+ id +"']").click(function(){
        var case_name = this.innerHTML;
        var test_case_url = $("#test_case_url").val() + case_name + "/";
        my_async_request(test_case_url, "GET", null, get_test_case_success);
    });
}

function get_test_case_list_success(data){
    var div_test_case = $("#div_test_case");
    var case_list = data.data.case;
    for(var index in case_list){
        add_case_node(case_list[index]);
    }

    var reg_env = new RegExp("(&|^)env_name=([^&]*)(&|$)");
    var env_name = window.location.search.substr(1).match(reg_env);
    if(env_name != null)
    {
        var env_option = $('#test_env option');
        for(var i=0;i<env_option.length;i++){
            if(decodeURI(env_name[2]) == env_option[i].innerHTML){
                env_option[i].selected = true;
                break;
            }
        }
    }
    var reg = new RegExp("(&|^)case_name=([^&]*)(&|$)");
    var case_name = window.location.search.substr(1).match(reg);
    if(case_name != null){
        var test_case_url = $("#test_case_url").val() + case_name[2] + "/";
        my_async_request(test_case_url, "GET", null, get_test_case_success);
    }
}

function get_test_case_list(){
    var test_case_url = $("#test_case_url").val();
    my_async_request(test_case_url, "GET", null, get_test_case_list_success);
}

$(function(){
    get_test_case_list();
});