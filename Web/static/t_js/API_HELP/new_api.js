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
}
$("#api_module").options[0].selected = true;
