/**
 * Created by msg on 11/3/15.
 */

function change_care(){
    var change_url = $("#care_url").val();
    if ($("#make_care").text() == "关注")
    {
        new_care(change_url);
    }
    else if($("#make_care").text() == "取消关注")
    {
        remove_care(change_url);
    }
}

function change_care_success(data){
    if ($("#make_care").text() == "关注")
    {
        $("#make_care").text("取消关注");
        $("#api_care_user").append('<span id="mine_care">我</span>');
    }
    else if($("#make_care").text() == "取消关注")
    {
        $("#make_care").text("关注");
        $("#mine_care").remove();
    }
}

function new_care(new_url){
    var api_no = $("#api_no").val();
    my_async_request(new_url, "POST", {api_no: api_no}, change_care_success);
}

function remove_care(remove_url){
    var api_no = $("#api_no").val();
    my_async_request(remove_url, "DELETE", {api_no: api_no}, change_care_success);
}

function add_param(data, param_pos) {
    var add_tr = $("<tr></tr>");
    add_tr.append(new_td("param", data));
    var necessary_td = new_td("necessary", data);
    necessary_td.addClass("text-center");
    add_tr.append(necessary_td);
    if (param_pos == "body") {
        var type_td = new_td("type", data);
        type_td.addClass("text-center");
        add_tr.append(type_td);

        if (data.status == 2) {
            //add_tr.addClass("grayBg");
            add_tr.find("td").first().append("【待废弃】");
        }
        else if (get_timestamp2() - data.update_time < 60 * 60 * 24 * 7) {
            if (datetime_2_timestamp(data.add_time) != data.update_time) {
                add_tr.find("td").first().append("【最近更新】");
            }
        }
    }
    add_tr.append(new_td("param_desc", data));
    $("#api_" + param_pos + "_param").append(add_tr);
}

function add_example(data, sign) {
    var add_div = $("<div></div>");
    var desc_p = $("<p></p>");
    desc_p.text(data[sign + "_desc"]);
    var example_p = $('<p><textarea class="form-control" readonly>' + data[sign + "_example"] + '</textarea></p>');
    add_div.append(desc_p);
    add_div.append(example_p);
    $("#api_" + sign + "_exist").append(add_div);
}

function init_api_info(data) {
    if (data == null) {
        my_async_request2(location.href, "GET", null, init_api_info);
        return;
    }
    var api_info = data.api_info;

    console.info(api_info);
    // basic info
    var keys = ["api_title", "api_url", "api_method", "api_desc", "stage", "add_time", "update_time"];
    var key_len = keys.length;
    for (var i = 0; i < key_len; i++) {
        $("#span_" + keys[i]).text(api_info.basic_info[keys[i]]);
    }
    // predefine header
    var ph_len = api_info.predefine_param.header.length;
    for (var i = 0; i < ph_len; i++) {
        var ph_key = api_info.predefine_param.header[i];
        if (ph_key in api_info.predefine_header) {
            var ph_data = api_info.predefine_header[ph_key];
            add_param(ph_data, "header");
        }
    }
    // header
    var header_len = api_info.header_info.length;
    for (var i = 0; i < header_len; i++) {
        add_param(api_info.header_info[i], "header");
    }
    // predefine body
    if (api_info.basic_info.api_method == "GET") {
        $("#api_body_param").find("caption").text("请求URL参数");
    }
    var pb_len = api_info.predefine_param.body.length;
    for (var i = 0; i < pb_len; i++) {
        var pb_key = api_info.predefine_param.body[i];
        if (pb_key in api_info.predefine_body) {
            var pb_data = api_info.predefine_body[pb_key];
            pb_data["status"] = 1;
            add_param(pb_data, "body");
        }
    }
    // body
    var body_len = api_info.body_info.length;
    for (var i = 0; i < body_len; i++) {
        add_param(api_info.body_info[i], "body");
    }

    if (ph_len + header_len == 0) {
        $("#api_header_param").hide();
    }
    if (pb_len + body_len == 0) {
        $("#api_body_param").hide();
    }

    // input
    var input_len = api_info.input_info.length;
    for (var i = 0; i < input_len; i++) {
        var input_item = api_info.input_info[i];
        add_example(input_item, "input");
    }
    // output
    var output_len = api_info.output_info.length;
    for (var i = 0; i < output_len; i++) {
        var output_item = api_info.output_info[i];
        add_example(output_item, "output");
    }

    if (input_len == 0) {
        $("#div_api_input").hide();
    }
    if (output_len == 0) {
        $("#div_api_output").hide();
    }
    // care
    var care_info = api_info.care_info;
    for (var i = 0; i < care_info.length; i++) {
        if (care_info[i]["user_name"] == $("#current_user_name").val()) {
            $("#api_care_user").append('<span id="mine_care">我</span>');
            if (care_info[i]["level"] == 0) { // 关注level为0 为API创建者不可取消关注
                $("#make_care").hide();
                $("#btn_del_api").show();
                $("#btn_del_api").click(function () {
                    my_request($("#del_api_url").val(), "DELETE")
                });
            }
            else {
                $("#make_care").text("取消关注");
            }
        }
        else {
            $("#api_care_user").append('<span>' + care_info[i]["nick_name"] + '</span>');
        }
    }
}

$(function() {
    init_api_info();
    var current_user_name = $("#current_user_name").val();

    var current_user_role = parseInt($("#current_user_role").val());
    var role_value = JSON.parse($("#role_value").text());
    if(bit_and(current_user_role, role_value["api_new"])){
        $("#a_update_api").attr("href", location.href + "&update=");
        $("div[id^='div_api_new_']").show();
    }

    $("#link_copy_location").click(function(){
        copy_text(location.href);
    });
});