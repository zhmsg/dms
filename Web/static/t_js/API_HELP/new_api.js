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
function rTrim(str, c){
    var s_len = str.length;
    for(var i=s_len-1;i>=0;i--){
        if(str[i] != c){
            return str.substr(0, i+1);
        }
    }
    return "";
}
function lTrim(str, c){
    var s_len = str.length;
    for(var i=0;i<s_len;i++){
        if(str[i] != c){
            return str.substr(i, s_len-i);
        }
    }
    return "";
}
function show_comp_url(){
    var selected_module = $("#api_module option:selected");
    var prefix = rTrim(selected_module.attr("title"), "/");
    var input_url = lTrim($("#api_url").val(), "/");
    $("#api_comp_url").text(prefix + "/" + input_url);
}


