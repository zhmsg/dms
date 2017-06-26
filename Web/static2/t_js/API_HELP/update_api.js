/**
 * Created by msg on 11/3/15.
 */

function add_body_success(data) {
    var tr_id = "trb_" + data.api_no + data.param;
    $("#" + tr_id).remove();
    var add_tr = $("<tr></tr>");
    add_tr.attr("id", tr_id);

    var param_td = $("<td></td>");
    param_td.text(data.param);
    add_tr.append(param_td);

    var necessary_td = $("<td></td>");
    if (data.necessary == true) {
        necessary_td.text("是");
    }
    else {
        necessary_td.text("否");
    }
    add_tr.append(necessary_td);

    var sign = "header";

    if ("type" in data) {
        var type_td = $("<td></td>");
        type_td.text(data.type);
        add_tr.append(type_td);
        sign = "body";
    }

    var desc_td = $("<td></td>");
    desc_td.text(data.param_desc);
    add_tr.append(desc_td);

    if (sign == "body") {
        var status_td = $("<td></td>");
        status_td.text(["稍后", "立即", "待废弃", "废弃"][data.status]);
        add_tr.append(status_td);
    }

    var op_td = $("<td></td>");
    var up_btn = $("<button class='btn btn-success'>更新</button>");
    var del_btn = $("<button class='btn btn-danger'>删除</button>");
    del_btn.attr("param_type", sign);
    if (sign == "body") {
        up_btn.click(update_body_param);
    }
    del_btn.click(delete_param);
    op_td.append(up_btn);
    op_td.append(" ");
    op_td.append(del_btn);
    add_tr.append(op_td);

    var tr = $("#api_" + sign + "_param tr").eq(-2);
    tr.after(add_tr);

    $("#" + sign + "_param_name").val("");
    $("#" + sign + "_param_desc").val("");
    $("#" + sign + "_param_type").val("");
    $("#btn_new_" + sign).text("新建");

    $("#btn_new_" + sign).removeClass();
    $("#btn_new_" + sign).addClass("btn btn-info");
}


function add_example_info() {
    var current_btn = $(this);
    var parent_div = current_btn.parent();
    var data = package_input(parent_div);
    my_async_request2(data["url"], "POST", data, add_example);
}

function add_api_info(type) {
    var request_url = $("#url_prefix").val() + "/" + type + "/";
    var id_prefix = type + "_param_";
    var post_params = $("[id^=" + id_prefix + "]");
    var request_data = new Object();
    for (var i = 0; i < post_params.length; i++) {
        var one_param = post_params[i];
        request_data[one_param.id.substring(id_prefix.length)] = one_param.value;
    }
    my_async_request2(request_url, "POST", request_data, add_body_success);
    console.info(request_data);
}

function delete_param() {
    var parent_tr = $(this).parent().parent();
    var tds = parent_tr.find("td");
    var param = tds[0].innerHTML;
    var param_type = $(this).attr("param_type");
    var del_url = $("#del_" + param_type + "_url").val();
    var request_data = JSON.stringify({"param": param});
    my_async_request2(del_url, "DELETE", {"param": param}, function () {
        parent_tr.remove();
    });
}

function delete_example() {
    var current_btn = $(this);
    var example_no = current_btn.attr("example_no");
    my_async_request2("/dev/api/example/", "DELETE", {"example_no": example_no}, function () {
        $("#example_" + example_no).remove();
    });
}


function format_input(input_id) {
    var input_content = $("#" + input_id).val();
    var json_content = JSON.stringify(JSON.parse(input_content), null, 4);
    $("#" + input_id).val(json_content);
}

function handler_success(data) {
    var btn_id = "pp_" + data.data["param"];
    var btn = $("#" + btn_id);
    var inner_value = btn.text();
    if (inner_value.indexOf("不需要") == 0) {
        var class_name = "btn btn-info";
        var inner_value = inner_value.replace("不", "");
    }
    else {
        var class_name = "btn btn-danger";
        inner_value = inner_value.replace("需要", "不需要");
    }
    btn.text(inner_value);
    btn.removeClass();
    btn.addClass(class_name);
}

function handle_predefine_param() {
    var btn = $(this);
    var param_type = btn.attr("param_type");
    var update_url = $("#url_prefix").val() + "/" + param_type + "/";
    var inner_value = btn.text();
    var param = btn.val();
    if (inner_value.indexOf("不需要") == 0) {
        var update_type = "delete";
    }
    else {
        var update_type = "new";
    }
    my_async_request(update_url, "PUT", {
        param: param,
        update_type: update_type,
        param_type: param_type
    }, handler_success);
}

function send_message() {
    alert("即将离开");
}

function update_body_param() {
    var parent_tr = $(this).parent().parent();
    var tds = parent_tr.find("td");
    $("#body_param_name").val(tds[0].innerHTML);
    select_option("body_param_necessary", tds[1].innerHTML, "text");
    select_option("body_param_type", tds[2].innerHTML, "text");
    $("#body_param_desc").val(tds[3].innerHTML);
    select_option("body_param_status", tds[4].innerHTML, "text");
    $("#btn_new_body").text("更新");
    $("#btn_new_body").removeClass();
    $("#btn_new_body").addClass("btn btn-success");
}

function update_stage(stage) {
    var update_url = $("#update_stage_url").val();
    my_async_request(update_url, "PUT", {"stage": stage});
}

function add_example(data) {
    var add_div = $("<div></div>");
    add_div.attr("id", "example_" + data.example_no);
    var desc_p = $("<p></p>");
    desc_p.text(data["example_desc"]);
    var example_p = $('<p><textarea class="form-control" readonly>' + data["example_content"] + '</textarea></p>');
    var op_p = $("<p></p>");
    var btn_update = $('<button class="btn btn-success">更新</button>');
    var btn_del = $('<button class="btn btn-danger">删除</button>');
    btn_del.attr("example_no", data.example_no);
    btn_del.click(delete_example);
    op_p.append(btn_update);
    op_p.append(btn_del);
    add_div.append(desc_p);
    add_div.append(example_p);
    add_div.append(op_p);
    if (data.example_type == 1) {
        $("#api_input_exist").append(add_div);
    }
    else if (data.example_type == 2) {
        $("#api_output_exist").append(add_div);
    }
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
    var stage = api_info.basic_info.stage;
    var update_url = $("#update_stage_url").val();
    if (stage == "新建" || stage == "修改中") {
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(2);">设置完成</a>');
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(3);">设置待废弃</a>');
    }
    else if (stage == "已完成") {
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(1);">设置修改中</a>');
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(3);">设置待废弃</a>');

    }
    if (stage != "已废弃" && stage != "已删除") {
        $("#span_modify_stage").append('<a class="margin10" href="javascript:void(0)" onclick="update_stage(4);">设置废弃</a>');
    }

    // predefine
    var pre = ["header", "body"];
    var pre_len = pre.length;
    for (var i = 0; i < pre_len; i++) {
        var param_type = pre[i];
        for (var key in api_info["predefine_" + param_type]) {
            var pb_item = api_info["predefine_" + param_type][key];
            var btn = $('<button></button>');
            btn.attr("id", "pp_" + pb_item.param);
            btn.attr("title", pb_item.param_desc);
            btn.val(pb_item.param);
            btn.attr("param_type", param_type);
            if ($.inArray(pb_item.param, api_info.predefine_param[param_type]) >= 0) {
                btn.addClass("btn btn-danger");
                btn.text("不需要" + pb_item.param);
            }
            else {
                btn.addClass("btn btn-info");
                btn.text("需要" + pb_item.param);
            }
            btn.addClass("margin5");
            btn.click(handle_predefine_param);
            $("#api_" + param_type + "_param").after(btn);
        }
        var l = api_info[param_type + "_info"].length;
        for (var j = 0; j < l; j++) {
            add_body_success(api_info[param_type + "_info"][j]);
        }
    }

    // examples
    var example_len = api_info.examples.length;
    for (var i = 0; i < example_len; i++) {
        var example_item = api_info.examples[i];
        add_example(example_item);
    }
}

$(function () {
    init_api_info();
    $("button[name='btn_new']").click(add_example_info);
});