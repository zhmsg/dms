/**
 * Created by msg on 11/3/15.
 */

var param_vm = null;


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
        if(example_item["example_type"] == 1){
            param_vm.all_input_examples.push(example_item);
        }
        else if(example_item["example_type"] == 2){
            param_vm.all_output_examples.push(example_item);
        }
    }
    // body info
    var param_len = api_info.body_info.length;
    var location_map = {"header": "header", "body": "body", "url": "url", "url_args": "url_args"};
    for(var k=0;k<param_len;k++){
        var p_item = api_info.body_info[k];
        if(p_item["location"] in location_map){
            p_item["location_name"] = location_map[p_item["location"]]
        }
        else{
            for(var kk=0;kk<param_len;kk++){
                var pp_item = api_info.body_info[kk];
                if(p_item["location"] == pp_item["param_no"]){
                    p_item["location_name"] = pp_item["param_name"];
                }
            }
        }
        param_vm.all_api_params.push(p_item);
    }
    param_vm.update_location();
}

$(function () {
    var param_url = "/dev/api/param";
    var example_url = "/dev/api/example";
    param_vm = new Vue({
        el: "#div_content",
        data: {
            all_api_params: [],
            all_location: [],
            all_input_examples: [],
            all_output_examples: [],
            //about param
            default_location: "body",
            current_location: "body",
            current_param_name: "",
            current_necessary: "1",
            current_type: "",
            current_desc: "",
            current_status: "1",
            //about input example
            i_example: {"desc": "", "content": ""},
            // about output example
            o_example: {"desc": "", "content": ""}

        },
        methods: {
            update_location: function(){
                var l = this.all_api_params;
                var tj = {};
                var len_p = this.all_api_params.length;
                this.all_location = [];
                var pending_location = [];
                for(var j=0;j<len_p;j++){
                    var p_item = this.all_api_params[j];
                    if(!(p_item["location"] in tj)){
                        tj[p_item["location"]] = 0;
                    }
                    tj[p_item["location"]] = 1 + tj[p_item["location"]];
                    if(p_item["location"] == "body"){
                        if(p_item["param_type"] == "object"){
                            this.all_location.push(p_item);
                        }
                        else if(p_item["param_type"] == "list"){
                            pending_location.push(p_item);
                        }
                    }
                }
                var pl_len = pending_location.length;
                for(var k=0;k<pl_len;k++){
                    if(pending_location[k]["param_no"] in tj){
                        continue;
                    }
                    this.all_location.push(pending_location[k]);
                }

            },
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
                                    "necessary": this.current_necessary, "param_type": this.current_type,
                                    "param_desc": this.current_desc, "status": this.current_status};

                my_async_request2(param_url, "POST", param_data, function(data){
                    data["location_name"] = data["location_item"]["param_name"];
                    that.all_api_params.push(data);
                    that.current_location =  this.default_location;
                    that.current_param_name = "";
                    that.current_necessary = "1";
                    that.current_type = "";
                    that.current_desc = "";
                    that.current_status = "1";
                    that.update_location();
                });
            },
            update_param_action: function(index){
                var that = this;
                var param_data = this.all_api_params[index];
                my_async_request2(param_url, "PUT", param_data, function(data){
                    alert1("更新成功");
                    that.update_location();
                });
            },
            remove_param_action: function(index){
                var that = this;
                var param_no = that.all_api_params[index]["param_no"];
                my_async_request2(param_url, "DELETE", {"param_no": param_no}, function(data){
                    that.all_api_params.splice(index, 1);
                })
            },
            format_e_content: function(example_type){
                if(example_type== 1){
                    var json_content = JSON.stringify(JSON.parse(this.i_example.content), null, 4);
                    this.i_example.content = json_content;
                }
                else if(example_type == 2){
                    var json_content = JSON.stringify(JSON.parse(this.o_example.content), null, 4);
                    this.o_example.content = json_content;
                }

            },
            new_example: function(example_type){
                var that = this;
                var e_data = {"example_type": example_type};
                if(example_type == 1){
                    var e_item = this.i_example;
                }
                else{
                    var e_item = this.o_example;
                }
                e_data["desc"] = e_item.desc;
                e_data["content"] = e_item.content;
                my_async_request2(example_url, "POST", e_data, function(data){
                    if(example_type == 1){
                        that.all_input_examples.push(data);
                    }
                    else{
                        that.all_output_examples.push(data);
                    }
                    e_item.content = "";
                    e_item.desc = "";
                });

            },
            copy_example: function(example_type, index){
                if(example_type == 1){
                    var e_item = this.all_input_examples[index];
                    var e_current = this.i_example;
                }
                else{
                    var e_item = this.all_output_examples[index];
                    var e_current = this.o_example;
                }
                e_current.desc = e_item["example_desc"];
                e_current.content = e_item["example_content"];
            },
            remove_example: function(example_type, index){
                var that = this;
                if(example_type == 1){
                    var e_list = this.all_input_examples;
                }
                else{
                    var e_list = this.all_output_examples;
                }
                var example_no = e_list[index]["example_no"];
                my_async_request2(example_url, "DELETE", {"example_no": example_no}, function(data){
                    e_list.splice(index, 1);
                })
            }
        }
    });
    init_api_info();
});