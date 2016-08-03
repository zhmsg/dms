/**
 * Created by msg on 12/3/15.
 */

function test_api(){
    update_res("正在请求...");
    $("#btn_save_result").hide();
    var test_env = $("#test_env").val();
    var api_url = $("#api_url").val();
    var api_method = $("#api_method").val();
    var request_url = test_env + api_url;
    if($("#request_url").val() != ""){
        request_url = $("#request_url").val();
    }
    else{
        update_res("无效的请求URL");
        return false;
    }
    var test_case_info = get_param_value();
    if(test_case_info == false){
        return;
    }
    var header_param = test_case_info.header;
    for(var param_key in header_param) {
        var param_value = header_param[param_key];
        if (param_key == "authorization") {
            header_param[param_key] = "Basic " + base64encode(param_value);
        }
        else if (param_key == "X-Authorization") {
            header_param[param_key] = "OAuth2 " + param_value;
        }
        else {
            header_param[param_key] = param_value;
        }
    }
    var body_param = test_case_info.body;
    if(api_method != "GET"){
        body_param = JSON.stringify(body_param)
    }
    $.ajax({
        url: request_url + "?geneacdms=test",
        method: api_method,
        contentType: "application/json",
        headers: header_param,
        //processData: false,
        data: body_param,
        success:function(data){
            console.info(data);
            if(typeof(data) == "string")
            {
                console.info("return json string");
                data = JSON.parse(data);
            }
            update_res(JSON.stringify(data, null, 4));
            $("#expect_status").val(data.status);
            update_status_url(data.status);
            $("#btn_save_result").show();
            $("#btn_save_result").text($("#btn_save_result").val());
            $("#save_name").hide();
        },
        error:function(xhr){
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            update_res(res);
            console.info(xhr);
        }
    });
}

function get_param_value(){
    var param_el = $("input[id$='_value']");
    var body_param = new Object();
    var header_param = new Object();
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
            var type = el.attributes["type"].value;
            if(type == "int"){
                param_value = Number(param_value);
                if(isNaN(param_value)){
                    update_res("无效的" + param_key);
                    return false;
                }
            }
            else if(type == "object" || type == "list"){
                console.info(param_value);
                try {
                    param_value = JSON.parse(param_value);
                }
                catch(e){
                    update_res("无效的" + param_key);
                    return false
                }
                console.info(param_value);
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
    var test_case_info = {body: body_param, header: header_param, url: url_param};
    return test_case_info;

}

function save_test_case_success(data){
    update_res(JSON.stringify(data, null, 4));
}

function save_test_case(){
    var case_name = $("#test_case_name").val();
    var expect_status = $("#expect_status").val();
    var test_case_info = get_param_value();
    if(test_case_info == false) {
        return;
    }
    update_res(JSON.stringify(test_case_info, null, 4));
    var test_case_url = $("#test_case_url").val();
    test_case_info["case_name"] = case_name;
    test_case_info["expect_status"] = parseInt(expect_status);
    my_async_request(test_case_url, "POST", test_case_info, save_test_case_success);
}

function get_test_case_success(data){
    if(data.status != true){
        update_res(JSON.stringify(data, null, 4));
    }
    var case_info = data.data;
    if("header" in case_info){
        for(var key in case_info.header){
            var v = case_info.header[key];
            if(v instanceof  Array || v instanceof Object) {
                $("#" + key + "_value").val(JSON.stringify(v));
            }
            else{
                $("#" + key + "_value").val(v);
            }
        }
    }
    if("body" in case_info){
        for(var key in case_info.body){
            var v = case_info.body[key];
            if(v instanceof  Array || v instanceof Object) {
                $("#" + key + "_value").val(JSON.stringify(v));
            }
            else{
                $("#" + key + "_value").val(v);
            }
        }
    }
    if("url" in case_info){
        for(var key in case_info.url){
            $("#url_value_" + key).val(case_info.url[key]);
        }
    }
    update_request_url();
    update_res("加载保存的测试用例 " + case_info.case_name + " 成功");
    $("#test_case_name").val(case_info.case_name);
}

function get_test_case_list_success(data){
    if(data.status != true){
        update_res(JSON.stringify(data, null, 4));
    }
    var div_test_case = $("#div_test_case");
    for(var index in data.data){
        div_test_case.append('<a href="javascript:void(0)" class="test_case">' + data.data[index] + '</a>');
    }
    $("a[class='test_case']").click(function(){
        var case_name = this.innerHTML;
        var test_case_url = $("#test_case_url").val() + case_name + "/";
        my_async_request(test_case_url, "GET", null, get_test_case_success);
    });
    var reg = new RegExp("(&|^)case_name=([^&]*)(&|$)");
    var case_name = window.location.search.substr(1).match(reg);
    if(case_name != null){
        var test_case_url = $("#test_case_url").val() + case_name[2] + "/";
        my_async_request(test_case_url, "GET", null, get_test_case_success);
    }
}

function get_test_case_list(){
    var test_case_url = $("#test_case_url").val();
    my_async_request(test_case_url, "GET", null, get_test_case_list_success);
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
            DownloadJson(file_name + ".json", $("#res_text").text());
            $("#save_name").val("");
            $("#btn_save_result").hide();
        }
    });
    get_test_case_list();
});

function update_res(s){
    $("#res_text").text(s);
    var a_h = "data:application/json;charset=utf-8," + encodeURIComponent(s);
    var a_s =$("#save_local");
    a_s.attr("href", a_h);
    a_s.attr("download", "sdfsd");

}

function update_request_url(){
    var test_env = $("#test_env").val();
    if(test_env == null){
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
        //alert(up.attributes["origin_param"].value);
    }
    $("#request_url").val(request_url);
}

function update_status_url(status_code){
    status_code = fill_zero(status_code, 8);
    var look_status = $("#look_status");
    console.info(look_status);
    var title = look_status.attr('title');
    $("#look_status").attr("href", title + "&status=" + status_code);
}

update_request_url();

function fill_zero(num, for_len) {
    var num_str = "" + num;
    while (for_len > 1){
        for_len -= 1;
        num /= 10;
        if (num >= 1) {
            continue
        }
        else{
            num_str = "0" + num_str;
        }
    }
    return num_str
}



