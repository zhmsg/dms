/**
 * Created by msg on 3/18/16.
 */

function Load_API_Module(data){
    var part_len = data.length;
    for(var i=0;i<part_len;i++){
        var module_list = data[i].module_list;
        var module_len = module_list.length;
        for(var j=0;j<module_len;j++){
            var module_item = module_list[j];
            add_option("target_api_module", module_item["module_no"], module_item["module_name"], module_item["module_desc"]);
            add_option("source_api_module", module_item["module_no"], module_item["module_name"], module_item["module_desc"]);
        }
    }
}

function target_api_info(data){
    var api_info = data.api_info;
    sessionStorage.setItem("dms_api_info_" + api_info["basic_info"]["api_no"], JSON.stringify(api_info));
    var module_no = api_info.basic_info.module_no;
    query_option("target_api_module", module_no, "value").attr("selected", true);
    query_option("source_api_module", module_no, "value").attr("selected", true);
    $("#target_api_module").attr("disabled", "disabled");
    $("#source_api_module").attr("disabled", "disabled");
    $("#div_source_api_module").hide();
}

function add_param_success(data) {
    console.info(data);
    var d_len = data.length;
    var t_id = "t_source_api_param";
    var t = $("#" + t_id);
    for (var i = 0; i < d_len; i++) {
        var d_item = data[i];
        var param_name = d_item["param"];
        console.info(param_name);
        console.info(t.find("tr[name='tr_" + param_name + "'] td[name='td_op']"));
        t.find("tr[name='tr_" + param_name + "'] td[name='td_op']").text("复制成功");
    }

}

function source_api_info(data, api_no)
{
    if(data == null){
        var api_info_str = sessionStorage.getItem("dms_api_info_" + api_no);
        if(api_info_str == null) {
            var info_url = $("#info_url").val() + "?api_no=" + api_no;
            my_request2(info_url, "GET", null, source_api_info);
            return true;
        }
        else{
            var api_info  = JSON.parse(api_info_str);
        }
    }
    else{
        api_info = data.api_info;
        sessionStorage.setItem("dms_api_info_" + api_info["basic_info"]["api_no"], JSON.stringify(api_info));
    }
    var t_params = $("#t_source_api_param");
    clear_table("t_source_api_param");
    var body_params = api_info.body_info;
    var params_len = body_params.length;
    var keys = ["param", "necessary", "type", "param_desc"];
    for(var i=0;i<params_len;i++){
        var param_item = body_params[i];
        var add_tr = $("<tr></tr>");
        add_tr.attr("name", "tr_" + param_item["param"]);
        for(var j=0;j<4;j++)
            add_tr.append(new_td(keys[j], param_item));
        add_tr.append('<td name=td_op><button class="btn btn-success copy_param">复制</button></td>');
        t_params.append(add_tr);
    }
    $(".copy_param").click(function(){
        $(this).attr("disabled", "disabled");
        var parent_tr = $(this).parents("tr");
        var r_data = {};
        r_data["name"] = parent_tr.find("td[name='td_param']").text();
        r_data["necessary"] = parent_tr.find("td[name='td_necessary']").text();
        r_data["type"] = parent_tr.find("td[name='td_type']").text();
        r_data["desc"] = parent_tr.find("td[name='td_param_desc']").text();
        if (r_data["necessary"] == "true") {
            r_data["necessary"] = 1;
        }
        else {
            r_data["necessary"] = 0;
        }
        var r_url = $("#body_url").val();
        my_async_request2(r_url, "POST", r_data, add_param_success);
    });
}

function Get_API_List_Success(data)
{
    var api_list = data.api_list;
    var api_len = api_list.length;
    for(var i=0;i<api_len;i++){
        var api_item = api_list[i];
        add_option("target_api_title", api_item["api_no"], api_item["api_title"], api_item["api_desc"]);
        add_option("source_api_title", api_item["api_no"], api_item["api_title"], api_item["api_desc"]);
    }
}

function get_api_list(module_no)
{
    var request_url = $("#module_url").val() + "?module_no=" + module_no;
    my_request2(request_url, "GET", null, Get_API_List_Success);
}


$(function(){
    var request_url = $("#module_url").val();
    my_request2(request_url, "GET", null, Load_API_Module);
    var api_no = UrlArgsValue(window.location.toString(), "api_no");
    if(api_no != null) {
        var info_url = $("#info_url").val() + "?api_no=" + api_no;
        var api_info_str = sessionStorage.getItem("dms_api_info_" + api_no);

        if(api_info_str == null) {
            my_request2(info_url, "GET", null, target_api_info);
        }
        else{
            var api_info  = JSON.parse(api_info_str);
            target_api_info({"api_info": api_info});
        }
    }
    get_api_list($("#source_api_module").val());
    query_option("target_api_title", api_no, "value").attr("selected", true);
    $("#target_api_title").attr("disabled", "disabled");
    query_option("source_api_title", api_no, "value").hide();

    $("#source_api_title").change(function(){
        source_api_info(null, $("#source_api_title").val());
    });
});