/**
 * Created by msg on 10/27/16.
 */

function Load_API_Module(data)
{
    module_data = data.data;
    var url_prefix = $("#url_prefix").val();
    for(var i=0;i<module_data.length;i++){
        var part_info = module_data[i];
        var add_part_div = $('<div class="apiMode api-help-mode"></div>');
        add_part_div.append('<div style="margin-bottom: 10px"><b>【' + part_info["part_desc"] + '】</b><br /></div>');
        for(var j=0;j<part_info["module_list"].length;j++)
        {
            var module_info = part_info["module_list"][j];
            add_part_div.append('<a id="a_module_' + module_info["module_no"] + '" href="' + url_prefix + '/?module_no=' + module_info["module_no"] +'">' + module_info["module_name"] + '</a>');
        }
        $("#div_module_list").append(add_part_div);
        add_option("module_part", part_info["part_no"], part_info["part_name"]);
    }
}

function Load_Module_Info(load_type){
    if(load_type == "info") {
        $("#span_module_no").text(current_module["module_no"]);
        $("#span_module_name").text(current_module["module_name"]);
        $("#span_module_prefix").text(current_module["module_prefix"]);
        $("#span_module_desc").text(current_module["module_desc"]);
    }
    else{
        $("#div_api_list").hide();
        $("#div_api_new_add").show();
        $("#module_no").val(current_module["module_no"]);
        $("#module_name").val(current_module["module_name"]);
        $("#module_prefix").val(current_module["module_prefix"]);
        $("#module_desc").text(current_module["module_desc"]);
        console.info(current_module);
        $("#module_part").val(current_module["module_part"]);
        $("#btn_op_module").text("更新模块");
        $("#div_add_env span").click();
        var test_envs = current_module["module_env"].split("|");
        for(var i=0;i<test_envs.length;i++){
            $("#s_add_env").val(test_envs[i]);
            add_test_env();
        }
    }
}

function Load_API_List(api_list, module_prefix)
{
    var url_prefix = $("#url_prefix").val();
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
        api_info["api_url"] = escape(rTrim(module_prefix, "/") + "/" + lTrim(api_info["api_path"], "/"));
        var keys = ["api_title", "api_url", "api_method", "stage"];
        for(var j=0;j<keys.length;j++){
            var key = keys[j];
            add_tr.append(new_td(key, api_info));
        }
        add_tr.append('<td class="text-center"><a href="' + url_prefix + '/info/?api_no=' + api_info["api_no"] + '">查看</a> | <a href="' + url_prefix + '/test/?api_no=' + api_info["api_no"] + '">测试</a></td>');
    }
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


function Load_Test_Env(data){
    var env_list = data.data;
    for(var i=0;i<env_list.length;i++){
        var one_env = env_list[i];
        add_option("s_add_env", one_env["env_no"], one_env["env_name"], one_env["env_address"]);
    }
}
