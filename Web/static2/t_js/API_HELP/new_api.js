/**
 * Created by msg on 11/3/15.
 */
function select_change(){
    var selected_module = $("#api_module option:selected");
    $("#selected_no").text(selected_module.val());
    $("#selected_name").text(selected_module.text());
    $("#selected_prefix").text(selected_module.attr("title"));
    $("#selected_desc").text(selected_module.attr("about"));
    $("#module_no").val(selected_module.val());
    show_comp_url();
}

function show_comp_url(){
    var selected_module = $("#api_module option:selected");
    var prefix = rTrim(selected_module.attr("title"), "/");
    var input_url = lTrim($("#api_path").val(), "/");
    $("#api_comp_url").text(prefix + "/" + input_url);
}

function load_api_info(data){
    var basic_info = data.data.api_info.basic_info;
    console.info(basic_info);
    $("#api_module").val(basic_info["module_no"]);
    select_change();
    $("#api_title").val(basic_info["api_title"]);
    $("#api_path").val(basic_info["api_path"]);
    $("#api_method").val(basic_info["api_method"]);
    $("#api_desc").val(basic_info["api_desc"]);
    $("#btn_new_api").text("更新");
}


$(function(){
    var module_no = UrlArgsValue(window.location.toString(), "module_no");
    if(module_no != null){
        $("#api_module").val(module_no);
    }
    select_change();
    var api_no = UrlArgsValue(window.location.toString(), "api_no");
    if(api_no != null) {
        var request_url = "/dev/api/info/?api_no=" + api_no;
        my_async_request(request_url, "GET", null, load_api_info);
    }
    $("#btn_new_api").click(function() {
        var request_url = location.href;
        var method = "POST";
        var request_data = new Object();
        if(api_no != null){
            method = "PUT";
            request_data["api_no"] = api_no;
        }
        request_data["api_module"] = $("#api_module").val();
        request_data["api_title"] = $("#api_title").val();
        request_data["api_path"] = $("#api_path").val();
        request_data["api_method"] = $("#api_method").val();
        request_data["api_desc"] = $("#api_desc").val();
        my_async_request(request_url, method, request_data)
    });
});