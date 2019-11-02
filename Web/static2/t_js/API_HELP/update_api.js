/**
 * Created by msg on 11/3/15.
 */

var param_vm = null;


function add_example_info() {
    var current_btn = $(this);
    var parent_div = current_btn.parent();
    var data = package_input(parent_div);
    my_async_request2(data["url"], "POST", data, add_example);
}

function delete_example() {
    var current_btn = $(this);
    var example_no = current_btn.attr("example_no");
    my_async_request2("/dev/api/example/", "DELETE", {"example_no": example_no}, function () {
        $("#example_" + example_no).remove();
    });
}


function format_input() {
    var input_content = $(this).val();
    var json_content = JSON.stringify(JSON.parse(input_content), null, 4);
    $(this).val(json_content);
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
    btn.addClass("margin5")
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
    var btn_update = $('<button class="btn btn-success margin5">更新</button>');
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
    }

    // examples
    var example_len = api_info.examples.length;
    for (var i = 0; i < example_len; i++) {
        var example_item = api_info.examples[i];
        add_example(example_item);
    }
    // body info
    var param_len = api_info.body_info.length;
    for(var k=0;k<param_len;k++){
        param_vm.all_api_params.push(api_info.body_info[k]);
    }
}

$(function () {
    init_api_info();
    $("button[name='btn_new']").click(add_example_info);
    $("textarea").change(format_input);
    $("textarea").keyup(format_input);
    var param_url = "/dev/api/param"
    param_vm = new Vue({
        el: "#api_params",
        data: {
            all_api_params: [],
            all_location: [],
            current_location: "body",
            current_param_name: "",
            current_necessary: "1",
            current_type: "",
            current_desc: "",
            current_status: "1"
        },
        methods: {
            new_param_action: function(){
                if(this.current_param_name.length <= 0){
                    alert_error("请设置 参数名称");
                    return false;
                }
                if(this.current_necessary == ""){
                    alert_error("请选择 参数是否必须");
                    return false;
                }
                if(this.current_type == ""){
                    alert_error("请选择 参数类型");
                    return false;
                }
                if(this.current_desc == ""){
                    alert_error("请设置 参数描述");
                    return false;
                }
                var that = this;
                var param_data = {"param_name": this.current_param_name, "location": this.current_location,
                                    "necessary": this.current_necessary, "type": this.current_type,
                                    "param_desc": this.current_desc, "status": this.current_status};

                my_async_request2(param_url, "POST", param_data, function(data){
                    that.all_api_params.push(data);
                    that.current_location =  "body";
                    console.info(that.current_location);
                    console.info(param_vm.current_location);
                    that.current_param_name = "";
                    that.current_necessary = "1";
                    that.current_type = "";
                    that.current_desc = "";
                    that.current_status = "1";
                });
            },
            update_param_action: function(index){
                var param_data = this.all_api_params[index];
                my_async_request2(param_url, "POST", param_data, function(data){
                    alert1("更新成功");
                });
            },
            remove_param_action: function(index){
                var that = this;
                var param_name = that.all_api_params[index]["param_name"];
                my_async_request2(param_url, "DELETE", {"param_name": param_name}, function(data){
                    that.all_api_params.splice(index, 1);
                })
            },
        }
    });
});