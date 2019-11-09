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
    $("#res_text").text(s);
}

function update_request_url(env_address){
    if(env_address == null) {
        var test_env = $("#test_env").val();
    }
    else{
        test_env = env_address;
    }
    if (test_env == null) {
        $("#request_url").val("");
        return;
    }
    var api_url = $("#api_url").val();
    var request_url = test_env + api_url;
    var url_param = $("input[id^='url_value_']");
    for(var i=0;i<url_param.length;i++){
        var up = url_param[i];
        var param_v = up.value;
        if(param_v == ""){
            continue;
        }
        var origin_param = up.attributes["origin_param"].value;
        request_url = request_url.replace(origin_param, param_v);
    }
    $("#request_url").val(request_url);
}

function update_status_url(status_code){
    status_code = fill_zero(status_code, 8);
    var look_status = $("#look_status");
    var title = look_status.attr('title');
    $("#look_status").attr("href", title + "&status=" + status_code);
}

function set_default_type()
{
    var type_select = $("select[name^='body_param_type_']");
    for(var i=0;i<type_select.length;i++){
        var one_select = type_select[i];
        var default_type = one_select.name.split("_")[3];
        one_select.value = default_type;
    }
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
    update_request_url();
    set_default_type();
    if($("#new_right").val() == "True"){
        new_right = true;
    }
    $("#authorization_value").parent().after('<li><input type="checkbox" id="skip_auth"> Skip Auth</li>');
    $("#Content-Type_value").val("application/json");
    $("#btn_generating_code").click(generating_code);

    var env_data = $("#lab_env_data").text();
    var test_envs = JSON.parse(env_data);
    var use_env = "";
    if(test_envs.length > 0){
        use_env = test_envs[0].env_address;
        update_request_url(use_env);
    }
    var te_vm = new Vue({
        el: "#p_env",
        data: {
            all_env: test_envs,
            use_env: use_env,
            custom_env: false
        },
        watch: {
            use_env: function(val){
                update_request_url(val);
            }
        }
    });
    params_vm = new Vue({
        el: "#div_params",
        data: {
            body_params: {},
        },
        methods: {
            test_api_action: function(){
                console.info(this.body_params);
            }
        },
        watch: {
            use_env: function(val){
                update_request_url(val);
            }
        }
    });
    var params_url = "/dev/api/param";
    my_async_request2(params_url, "GET", null, function(data){
        console.info(data);
        params_vm.body_params = data.body;
        console.info(params_vm.body_params);
    });
});



