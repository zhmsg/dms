/**
 * Created by msg on 10/27/16.
 */

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