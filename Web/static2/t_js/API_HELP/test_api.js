/**
 * Created by msg on 12/3/15.
 */

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

function update_res(s){
    $("#res_text").text(s);
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
});



