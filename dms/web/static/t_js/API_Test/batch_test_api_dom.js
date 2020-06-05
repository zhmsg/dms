/**
 * Created by msg on 8/5/16.
 */

function Add_Test(api_module_name, api_no, api_name, case_name)
{
    var OneTestInfo = "<div id='div_" + api_no + "_"+ case_name+"'>";
    OneTestInfo += '<div class="top_div">';
    OneTestInfo += '<span class="pull-left text-right width150">API模块：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + api_module_name + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150">API名称：</span>';
    OneTestInfo += '<input class="form-control bug-input" name="api_no" style="display: none" value="' + api_no + '"></input>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + api_name + '"></input>';
    OneTestInfo += '<span class="pull-left text-right width150" name="case_name">测试名称：</span>';
    OneTestInfo += '<input class="form-control bug-input" readonly value="' + case_name + '"></input>';
    OneTestInfo += '<span class="clear"></span>';
    OneTestInfo += "</div>";
    OneTestInfo += "</div>";
    $("#div_" + api_no).append(OneTestInfo);
}

function Add_Test_Info(server_name, api_no, case_name, api_url, id)
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
    $("#div_" + api_no + "_" + case_name).append(OneTestInfo);
}

function Notice_No_Case(api_no)
{
    var add_url = $("#one_test_url").val() + "?api_no=" + api_no;
    var info = "<div>";
    info += "<span class='error_result'>API " + API_Info[api_no].basic_info.api_title + " 还没有测试用例 </sapn>";
    info += '<a href="' + add_url + '">点击添加</a>';
    $("#div_" + api_no).append(info);
    $("#div_" + api_no).css("border", "none");
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
            $("#" + id).html('<span class="pull-left error_result">失败' + " 状态码：" + status_a + " 信息：" + message + '</span><a href="#" onclick="ReTest(this);">重新测试</a>');
        }
    }
    else
    {
        $("#" + id).html('<span class="pull-left error_result">失败' + " 状态码：" + status + " 信息：" + message + '</span><a href="#" onclick="ReTest(this);">重新测试</a>');
    }
}

function ReTest(el)
{
    var id = el.parentNode.id;
    var api_no = id.substr(12, 32);
    var case_name = id.substr(45).replace(/_\d$/g, "");
    var env_name = el.parentNode.parentNode.childNodes[1].innerText;
    var test_url = $("#one_test_url").val() + "?api_no=" + api_no + "&case_name=" + case_name + "&env_name=" + env_name;
    window.open(test_url);
}