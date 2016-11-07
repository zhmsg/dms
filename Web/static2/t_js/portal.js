/**
 * Created by msg on 10/20/16.
 */

function bit_and(role1, role2){
    var v = role1 & role2;
    if(v < role1 && v < role2)
        return false;
    else
        return true;
}

var menu_list = [["api_look", "api_url_prefix", "API文档"], ["status_code_look", "status_url_prefix", "API状态码"],
    ["table_look", "table_url_prefix", "数据表设计"], ["right_look", "right_url_prefix", "晶云平台操作权限"],
    ["param_look", "param_url_prefix", "晶云公共参数"], ["log_look", "log_url_prefix", "晶云平台日志"],
    ["release_ih_N", "release_ih_url_prefix", "重启晶云服务"], ["release_ytj_N", "release_ytj_url_prefix", "重启晶云服务"],
    ["bug_look", "bug_url_prefix", "BUG"], ["user_new", "register_url_prefix", "新建用户"],
    ["user_new", "authorize_url_prefix", "用户授权"]];

$(function(){
    var current_user_role = parseInt($("#current_user_role").val());
    if(current_user_role > 0) {
        var role_value = JSON.parse($("#role_value").text());
        var exist_menu = new Array();
        var exist_index = 0;
        for (var i = 0; i < menu_list.length; i++) {
            var menu_item = menu_list[i];
            if (exist_menu.indexOf(menu_item[2]) >= 0) {
                continue;
            }
            if (bit_and(current_user_role, role_value[menu_item[0]])) {
                $("#div_main_menu").append('<a href="' + $("#" + menu_item[1]).val() + '/">' + menu_item[2] + '</a>');
                exist_menu[exist_index] = menu_item[2];
                exist_index++;
            }
        }
        var current_href = location.href.substr((location.protocol + "//" + location.host).length);
        if(current_href.indexOf("/tornado") == 0){
            $("#div_current_env").append('<a href="' + current_href.substr(8) + '">' + '还用Flask' + '</a>');
        }
        else{
            $("#div_current_env").append('<a href="/tornado' + current_href + '">' + '体验Tornado' + '</a>');
        }
    }
    $("#div_main_menu").append('<a href="' + $("#password_url_prefix").val() + '/">' + '修改密码' + '</a>');
    $("#div_main_menu").append('<a href="' + $("#exit_url_prefix").val() + '/">' + '退出' + '</a>');
});