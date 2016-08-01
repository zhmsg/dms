/**
 * Created by msg on 8/1/16.
 */

function Add_Test_Info(server_name, api_module_name, api_name, api_url, result, status_code, message)
{
    var OneTestInfo = '<span class="pull-left text-right width150">服务环境：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + server_name + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150">API模块：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + api_module_name + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150">API名称：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + api_name + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150">请求URL：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + api_url + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150">测试结果：</span>';
    OneTestInfo += '<span class="pull-left">' + ' 成功' + ' 状态码：' + '1000001' + '</span>';
    $("#div_test_info").append(OneTestInfo);
}

Add_Test_Info("用户验证本地环境", "用户验证", "新建用户", "http://127.0.0.1:6011/auth/");