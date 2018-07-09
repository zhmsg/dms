/**
 * Created by msg on 10/27/16.
 */

function Load_API_Module(data)
{
    module_data = data.data;
    var url_prefix = $("#url_prefix").val();
    for(var i=0;i<module_data.length;i++){
        var part_info = module_data[i];
        m_vm.modules_data.push(part_info);
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
        api_info["api_url2"] = rTrim(module_prefix, "/") + "/" + lTrim(api_info["api_path"], "/");
        api_vm.api_list.push(api_info);
    }
    if(api_list.length > 10){
        $("#a_query_list").show();
    }
    else{
        $("#a_query_list").hide();
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
