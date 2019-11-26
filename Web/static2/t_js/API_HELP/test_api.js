/**
 * Created by msg on 12/3/15.
 */

var params_vm = null;
var new_right = false;

function fill_zero(num, for_len) {
    var num_str = "" + num;
    while (for_len > 1){
        for_len -= 1;
        num /= 10;
        if (num >= 1) {
            continue;
        }
        else{
            num_str = "0" + num_str;
        }
    }
    return num_str
}

function get_param_value(){
    var param_el = $("input[id$='_value']");
    var body_param = new Object();
    var header_param = new Object();
    var u_header_param = new Object();
    var url_param = new Object();
    for(var i=0;i<param_el.length;i++){
        var el = param_el[i];
        var id = el.id;
        var param_key = id.substr(0, id.indexOf("_value"));
        var param_value = el.value;
        if(param_value == ""){
            continue;
        }
        var param_type = el.attributes["param_type"].value;
        if(param_type == "body"){
            if(new_right == true){
                var type = $("#" + param_key + "_type").val();
            }
            else{
                var type = el.attributes["type"].value;
            }
            if(type == "int"){
                param_value = Number(param_value);
                if(isNaN(param_value)){
                    update_res("无效的" + param_key);
                    return false;
                }
            }
            else if(type == "object" || type == "list"){
                try {
                    param_value = JSON.parse(param_value);
                }
                catch(e){
                    update_res("无效的" + param_key);
                    return false
                }
            }
            else if (type == "bool"){
                if(param_value == "true"){
                    param_value = true;
                }
                else if(param_value == "false"){
                    param_value = false;
                }
                else{
                    update_res("无效的" + param_key);
                    return false;
                }
            }
            body_param[param_key] = param_value;
        }
        else if(param_type == "header"){
                header_param[param_key] = param_value;
        }
    }
    for (var param_key in header_param) {
        var param_value = header_param[param_key];
        if (param_key == "authorization") {
            if ($("#skip_auth").is(':checked')) {
                u_header_param["X-Skip-Auth"] = param_value.split(":")[0];
            }
            else {
                var auth_split = param_value.split(":");
                if (auth_split.length != 2) {
                    update_res("请输入正确的authorization,例如zh_test:123456");
                    return false;
                }
                u_header_param[param_key] = "Basic " + base64encode(param_value);
            }
        }
        else if (param_key == "X-Authorization") {
            if(param_value.indexOf("OAuth2 ") == 0){
                u_header_param[param_key] = param_value;
            }
            else {
                u_header_param[param_key] = "OAuth2 " + param_value;
            }
        }
        else {
            u_header_param[param_key] = param_value;
        }
    }
    var url_el = $("input[id^='url_value_']");
    for(var i=0;i<url_el.length;i++) {
        var el = url_el[i];
        var param_key = el.id.substr(10);
        var param_value = el.value;
        if (param_value == "") {
            continue;
        }
        url_param[param_key] = param_value;
    }
    var test_case_info = {body: body_param, header: header_param, url: url_param, u_header: u_header_param};
    return test_case_info;

}

function update_res(s){
    params_vm.output_info = s;
}

function update_request_url(env_address){
    if(env_address == undefined) {
        var test_env = params_vm.use_env;
    }
    else{
        test_env = env_address;
    }
    if (test_env == null) {
        params_vm.request_url = "";
        return;
    }
    var api_url = params_vm.basic_info.api_url;
    for(var index in params_vm.url_params.sub_params){
        var p = params_vm.url_params.sub_params[index];
        var v = p.param_value;
        if(v.length == 0){
            continue;
        }
        var reg = new RegExp("[<{]([a-z]*:?" + p.param_name + ")[}>]", "gi");
        api_url = api_url.replace(reg, v);
    }
    var request_url = test_env + api_url;
    //var url_param = $("input[id^='url_value_']");
    //for(var i=0;i<url_param.length;i++){
    //    var up = url_param[i];
    //    var param_v = up.value;
    //    if(param_v == ""){
    //        continue;
    //    }
    //    var origin_param = up.attributes["origin_param"].value;
    //    request_url = request_url.replace(origin_param, param_v);
    //}
    params_vm.request_url = request_url;
}

function update_status_url(status_code){
    status_code = fill_zero(status_code, 8);
    var look_status = $("#look_status");
    var title = look_status.attr('title');
    $("#look_status").attr("href", title + "&status=" + status_code);
}


function generating_code() {
    var test_case_info = get_param_value();
    var api_url = $("#api_url").val();
    var api_method = $("#api_method").val();
    var test_env = $("#test_env").val();
    var request_url = test_env + api_url;
    if ($("#request_url").val() != "") {
        request_url = $("#request_url").val();
    }
    else {
        update_res("无效的请求URL");
        return false;
    }
    var cmd = "import json\nimport requests\n";
    cmd += 'url = "' + request_url + '"\n';
    cmd += 'method = "' + api_method + '"\n';
    cmd += "headers = json.loads('" + JSON.stringify(test_case_info.u_header) + "')\n";
    cmd += "data = json.loads('" + JSON.stringify(test_case_info.body) + "')\n";
    if (api_method == "GET") {
        cmd += "resp = requests.request(method, url, headers=headers, params=data)\n";
    }
    else {
        cmd += "resp = requests.request(method, url, headers=headers, json=data)\n";
    }
    cmd += "assert resp.status_code == 200\n";
    cmd += "r_data = resp.json()\n";
    cmd += 'print "success" if r_data["status"] % 10000 < 100 else "status exception"\n';
    cmd += 'print(r_data["status"])\n';
    cmd += 'print(r_data["message"])\n';
    cmd += 'print r_data["data"] if "data" in r_data else "no data"\n';
    update_res(cmd);
}

function init_params(d){
    if("sub_params" in d){
        if(d["param_type"] == 'object'){
            var o = {};
            for(var key in d["sub_params"]){
                init_params(d['sub_params'][key]);
            }
            return o;
        }else{
            var l = [];
            d['sub_param_item'] = d['sub_params'][0];
            for(var i=0;i<d['sub_params'].length;i++){
                init_params(d['sub_params'][i]);
            }
            return l;
        }
    }
    d.param_value = "";
    d.value_error = "";
}

function extract_value(d){
    var ev_r = {'r': true, 'v': null};
    if("sub_params" in d){
        if(d["param_type"] == 'object'){
            var o = {};
            for(var key in d["sub_params"]){
                var sub_ev_r = extract_value(d['sub_params'][key]);
                if(sub_ev_r['r'] == false){
                    ev_r['r'] = false;
                }

                var sub_value = sub_ev_r['v'];
                if(typeof sub_value == 'object' || typeof sub_value == 'array'){
                    o[key] = sub_value;
                }
                else if(sub_value != null && sub_value != ""){
                    o[key] = sub_value;
                }
            }
            ev_r['v'] = o;
            return ev_r;
        }else{
            var l = [];
            for(var i=0;i<d['sub_params'].length;i++){
                var sub_ev_r = extract_value(d['sub_params'][i]);
                if(sub_ev_r['r'] == false){
                    ev_r['r'] = false;
                }
                l[i] = sub_ev_r['v'];
            }
            ev_r['v'] = l;
            return l;
        }
    }
    else if("param_value" in d){
        ev_r['v'] = d["param_value"];
        if(ev_r['v'] != "") {
            if (d["param_type"] == 'object' || d["param_type"] == 'list') {
                try {
                    var param_value = JSON.parse(d["param_value"]);
                    ev_r['v'] = param_value;
                }
                catch (e) {
                    ev_r['r'] = false;
                    d["value_error"] = "无效的" + d['param_name'];
                }
            }
        }
    }
    return ev_r;
}

function test_api22(){
    update_res("正在请求...");
    var api_method = params_vm.basic_info.api_method;
    var request_url = params_vm.request_url;
    if(request_url != ""){
    }
    else{
        update_res("无效的请求URL");
        return false;
    }

    var header_ev_r = extract_value(params_vm.tabs_class.header.params);
    if(header_ev_r['r'] == false){
        update_res("header 值存在设置错误");
        return false;
    }
    var header_param = header_ev_r['v'];

    var body_ev_r = extract_value(params_vm.tabs_class.body.params);
    if(body_ev_r['r'] == false){
        update_res("body 值存在设置错误");
        return false;
    }

    var body_param = body_ev_r['v'];

    var url_args_ev_r = extract_value(params_vm.tabs_class.url_args.params);
    if(url_args_ev_r['r'] == false){
        update_res("url args 值存在设置错误");
        return false;
    }
    var url_args = url_args_ev_r['v'];

    if(api_method != "GET"){
        if(typeof body_param == "object")
        {
            body_param = JSON.stringify(body_param);
        }
    }
    else{
        body_param = url_args;
    }
    var req = {
        url: request_url,
        method: api_method,
        contentType: "application/json",
        headers: header_param,
        data: body_param,
        success:function(data){
            if(typeof(data) == "string")
            {
                data = JSON.parse(data);
            }
            update_res(JSON.stringify(data, null, 4));
            params_vm.r_http_code = "";
            params_vm.r_http_text = "";
        },
        error:function(xhr){
            params_vm.r_http_code = xhr.status;
            params_vm.r_http_text = xhr.statusText;
            if(xhr.responseJSON){
                update_res(JSON.stringify(xhr.responseJSON, null, 4));
            }
            else{
                update_res(xhr.responseText);
            }
        }
    };
    if(header_param != null && header_param != ""){
        req['headers'] = header_param;
    }
    if(body_param != null && body_param != ""){
        req['data'] = body_param;
    }
    $.ajax(req);
}


function storage_action()
{
    if(params_vm == null){
        return;
    }
    if(params_vm.api_no == ""){
        return
    }
    var header_param = extract_value(params_vm.tabs_class.header.params)['v'];
    var body_param = extract_value(params_vm.tabs_class.body.params)['v'];
    var url_args = extract_value(params_vm.tabs_class.url_args.params)['v'];
    var url_param = extract_value(params_vm.url_params)['v'];
    var data = {'body': body_param, 'headers': header_param,
        'args': url_args, 'urls': url_param};
    save_api_test_example(params_vm.api_no, data);
}

function dict_value_copy(dest_d, source_d)
{
    if("sub_params" in dest_d) {
        if (typeof source_d == 'object' && dest_d.param_type == 'object') {
            for(var key in dest_d["sub_params"]){
                if(key in source_d){
                    dict_value_copy(dest_d["sub_params"][key], source_d[key])
                }
            }
        }
        else if (typeof source_d == 'array' && dest_d.param_type == 'list') {
            for(var i=0;i<source_d.length;i++){
                params_vm.add_sub_params(dest_d);
                dict_value_copy(dest_d.sub_params[dest_d.sub_params.length - 1], source_d[i]);
            }
        }
    }
    else{
        dest_d.param_value = source_d;
    }
}

function load_storage()
{
    if(params_vm == null || params_vm.api_no == ""){
        return;
    }
    var data = get_api_test_example(params_vm.api_no);
    if(data == null){
        return
    }

    dict_value_copy(params_vm.tabs_class.header.params, data.headers);
    dict_value_copy(params_vm.tabs_class.body.params, data.body);
    dict_value_copy(params_vm.tabs_class.url_args.params, data.args);
    dict_value_copy(params_vm.url_params, data.urls);
}

$(function(){
    $("#btn_save_case").click(function(){
        var btn_t = this.innerHTML;
        var btn_v = this.value;
        if(btn_t == btn_v){
            this.innerHTML = btn_v.substr(0, 2);
            $("#test_case_name").show();
            $("#expect_status").show();
        }
        else{
            this.innerHTML = btn_v;
            $("#expect_status").hide();
            $("#test_case_name").hide();
            var case_name = $("#test_case_name").val();
            if(case_name.length<=0 || case_name.length>15){
                update_res("未保存测试用例 \n测试用例的名称长度必须在1-15");
                return;
            }
            if(case_name.match(/[^\u4e00-\u9fa5\w\-]/g) != null){
                update_res("未保存测试用例 \n测试用例的名称仅允许汉字数字字母下划线(_)短横线(-)");
                return;
            }

            var expect_status = $("#expect_status").val();
            if(expect_status.length<=0 || expect_status.length>=8){
                update_res("未保存测试用例 \n测试用例期待的状态码必须在1-8");
                return;
            }
            if(expect_status.match(/[^\d]/g) != null){
                update_res("未保存测试用例 \n测试用例期待的状态码必须为正整数");
                return;
            }
            save_test_case();
        }
    });
    $("#btn_save_result").click(function(){
        var btn_t = this.innerHTML;
        var btn_v = this.value;
        if(btn_t == btn_v){
            this.innerHTML = btn_v.substr(0, 2);
            $("#save_name").show();

        }
        else{
            var file_name = $("#save_name").val();
            if(file_name.length<=0){
                return;
            }
            this.innerHTML = btn_v;
            $("#save_name").hide();
            DownloadFile(file_name + ".json", $("#res_text").text());
            $("#save_name").val("");
            $("#btn_save_result").hide();
        }
    });
    $("#btn_save_output").click(function(){
        var btn_t = this.innerHTML;
        var btn_v = this.value;
        if(btn_t == btn_v){
            this.innerHTML = btn_v.substr(0, 2);
            $("#output_desc").show();
        }
        else{
            this.innerHTML = btn_v;
            save_output_example();
            $("#btn_save_output").hide();
            $("#output_desc").hide();
        }
    });

    if($("#new_right").val() == "True"){
        new_right = true;
    }
    $("#authorization_value").parent().after('<li><input type="checkbox" id="skip_auth"> Skip Auth</li>');
    $("#Content-Type_value").val("application/json");
    $("#btn_generating_code").click(generating_code);

    params_vm = new Vue({
        el: "#div_params",
        data: {
            api_no: "",
            all_env: [],
            use_env: "",
            custom_env: false,
            basic_info: {},
            has_params: true,
            tabs_class: {"url_args": {"active": "", params: {}, "name": "Url args"},
                "body": {"active": "", params: {}, "name": "Body"},
                "header": {"active": "", "params": {}, "name": "Headers"}},
            params: {},
            url_params: {},
            request_url: "",
            output_info: "",
            r_http_code: "",
            r_http_text: ""
        },
        methods: {
            change_tab: function(key){
                for(var _key in this.tabs_class){
                    this.tabs_class[_key]['active'] = "";
                }
                if(key == ""){
                    this.has_params = false;
                    return false;
                }
                this.params = this.tabs_class[key]['params'];
                this.has_params = true;
                this.tabs_class[key]['active'] = "active";
            },
            update_url_action: function () {
                update_request_url();
            },
            test_api_action: function(){
                test_api22();
                storage_action();
            },
            add_sub_params: function(parent_item){
                var ns_item = {};
                var keys = ["param_name", "param_type", "necessary", "param_desc"];
                for(var k_i in keys){
                    var key = keys[k_i];
                    ns_item[key] = parent_item.sub_param_item[key];
                }
                parent_item.sub_params.push(ns_item);
                return ns_item
            },
            delete_sub_params: function(parent_item, index){
                parent_item.sub_params.splice(index, 1);
            }
        },
        watch: {
            use_env: function(val){
                update_request_url(val);
                return val;
            }
        }
    });

    var info_url = "/dev/api/info/";
    my_async_request2(info_url, "GET", null, function(data){
        params_vm.api_no = data.api_info.basic_info.api_no;
        document.title = data.api_info.basic_info.api_title;
        params_vm.basic_info = data.api_info.basic_info;
        var module_env = data.api_info.basic_info.module_env;
        var env_url = "/dev/api/test/env?env_no=" + module_env.replace("|", ",");
        my_async_request2(env_url, "GET", null, function(data){
            params_vm.all_env = data;
            if(data.length > 0){
                params_vm.use_env = data[0].env_address;
            }
        });
        load_storage();
    });
    var params_url = "/dev/api/param";
    my_async_request2(params_url, "GET", null, function(data){
        init_params(data.body);
        init_params(data.url_args);
        init_params(data.url);
        params_vm.tabs_class["url_args"].params = data.url_args;
        params_vm.tabs_class["body"].params = data.body;
        params_vm.tabs_class["header"].params = data.header;
        params_vm.url_params = data.url;
        if("sub_params" in data.url_args){
            params_vm.change_tab("url_args");
        }
        else if("sub_params" in data.body){
            params_vm.change_tab("body");
        }
        else if("sub_params" in data.header){
            params_vm.change_tab("header");
        }
        else{
            params_vm.change_tab("");
        }
        load_storage();
    });
});



