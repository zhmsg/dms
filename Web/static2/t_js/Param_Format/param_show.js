/**
 * Created by msg on 9/23/16.
 */

function clear_input_value()
{
    $("input[class*='data_input']").val("");
    $("textarea").val("");
    $("span[id^='tip_']").html("");
    param_type_change();
}

function param_type_change()
{
    var param_type = $("#param_type").val();
    var measure = "长度";
    $("tr[name^='tr_special']").hide();
    if(param_type == "unicode"){
        $("tr[name^='tr_special_unicode']").show();
    }
    else if(param_type == "int"){
        measure = "值";
    }
    $("#lab_min_len").text("最小" + measure);
    $("#lab_max_len").text("最大" + measure);
}

function add_success(data)
{
    Add_TR(data.data);
    clear_input_value();
    $("#close_popup").click();
}

function check_input_value()
{
    $("#btn_add_param").unbind('click');
    $("#btn_add_param").attr("disabled", "disabled");
    var param = $("#param").val();
    if(param.length <= 3){
        $("#tip_param").html('<p class="glyphicon glyphicon-exclamation-sign glyphicon-pink"></p>长度不可低于4位');
        return false;
    }
    var search_r = param.search(/\W+/i);
    if(search_r != -1){
        $("#tip_param").html('<p class="glyphicon glyphicon-exclamation-sign glyphicon-pink"></p>仅允许\\w');
        return false;
    }
    $("#tip_param").html('');

    var min_len = $("#min_len").val();
    if(min_len.length > 0){
        if(min_len.search(/\D+/i) != -1){
            $("#tip_min_len").html('<p class="glyphicon glyphicon-exclamation-sign glyphicon-pink"></p>请输入数字');
            return false;
        }
    }
    $("#tip_min_len").html('');

    var max_len = $("#max_len").val();
    if(max_len.length > 0){
        if(max_len.search(/\D+/i) != -1){
            $("#tip_max_len").html('<p class="glyphicon glyphicon-exclamation-sign glyphicon-pink"></p>请输入数字');
            return false;
        }
    }
    $("#tip_max_len").html('');

    var param_desc = $("#param_desc").val();
    if(param_desc.length <= 0){
        $("#tip_param_desc").html('<p class="glyphicon glyphicon-exclamation-sign glyphicon-pink"></p>描述不能为空');
        return false;
    }
    $("#tip_param_desc").html('');


    $("#btn_add_param").click(add_param);
    $("#btn_add_param").removeAttr("disabled");
    return true;
}

function click_update()
{
    var children_td = this.parentNode.parentNode.children;
    $("#param").val(children_td[0].innerHTML);
    $("#param_type").val(children_td[1].innerHTML);
    $("#min_len").val(children_td[2].innerHTML);
    $("#max_len").val(children_td[3].innerHTML);
    $("#not_allow").val(children_td[4].innerHTML);
    $("#match_str").val(children_td[5].innerHTML);
    $("#param_desc").val(children_td[6].innerHTML);
    check_input_value();
}

function add_param()
{
    if(check_input_value() == false){
        return;
    }
    var param = $("#param").val();
    if(param.length <= 3){
        $("#tip_param").html('<p class="glyphicon glyphicon-exclamation-sign glyphicon-pink"></p>名称不能为空！');
        return;
    }
    var param_type = $("#param_type").val();
    var param_desc = $("#param_desc").val();
    var add_values = $("input[name='add_value']:visible");
    var request_data = {param: param, param_type:param_type, param_desc:param_desc};
    for(var i=0;i<add_values.length;i++){
        var value_item = add_values[i];
        if(value_item.value.length > 0) {
            if(value_item.attributes["type"].value == "int"){
                request_data[value_item.id] = parseInt(value_item.value);
            }
            else{
                request_data[value_item.id] = value_item.value;
            }
        }
    }
    my_async_request(location.href, "POST", request_data, add_success);
}

function get_success(data){
    for(var i=0;i<data.data.length;i++){
        Add_TR(data.data[i]);
    }
}

$(function() {
    $("#param_type").change(param_type_change);
    $("input[class*='data_input']").change(check_input_value);
    $("textarea").change(check_input_value);
    my_async_request(location.href, "GET", null, get_success);
});