/**
 * Created by msg on 12/3/15.
 */

function test_api(){
    update_res("正在请求...");
    var test_env = $("#test_env").val();
    var api_url = $("#api_url").val();
    var api_method = $("#api_method").val();
    var request_url = test_env + api_url;
    if($("#request_url").val() != ""){
        request_url = $("#request_url").val();
    }
    console.info(request_url);
    var param_el = $("input[id$='_value']");
    var body_param = new Object();
    var header_param = new Object();
    //var xhr = new XMLHttpRequest();
    //xhr.open(api_method, request_url + "?geneacdms=test");
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
                param_value = JSON.parse(param_value);
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
            if(param_key == "authorization"){
                header_param[param_key] = "Basic " + base64encode(param_value);
            }
            else if (param_key == "X-Authorization")
            {
                header_param[param_key] = "OAuth2 " + param_value;
            }
            else{
                header_param[param_key] = param_value;
            }
            //xhr.setRequestHeader(param_key, header_param[param_key]);
        }
    }
    console.info(header_param);
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
            update_status_url(data.status);
        },
        error:function(xhr){
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            update_res(res);
            console.info(xhr);
        }
    });
}

function requestComplete(evt) {
    /* This event is raised when the server send back a response */
    console.log(evt.target.response);
    if(this.status==200){
        var res = evt.target.response;
        update_res(JSON.stringify(JSON.parse(res), null, 4));
    }else{
        update_res(this.status);
    }
}

function requestFailed(evt){
    console.info(evt);
}

function get_authorization_value(v){
    var cb = $('input:radio[name="auth_method"]:checked');
    if(cb == null){
        return v;
    }
    if(cb.val() == "Basic"){
        return "Basic " + base64encode(v);
    }
    else{
        return v;
    }

}

function update_res(s){
    $("#res_text").text(s);
}

function update_request_url(){
    var test_env = $("#test_env").val();
    var api_url = $("#api_url").val();
    var request_url = test_env + api_url;
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

var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var base64DecodeChars = new Array(-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);
/**
 * base64编码
 * @param {Object} str
 */
function base64encode(str){
    var out, i, len;
    var c1, c2, c3;
    len = str.length;
    i = 0;
    out = "";
    while (i < len) {
        c1 = str.charCodeAt(i++) & 0xff;
        if (i == len) {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt((c1 & 0x3) << 4);
            out += "==";
            break;
        }
        c2 = str.charCodeAt(i++);
        if (i == len) {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
            out += base64EncodeChars.charAt((c2 & 0xF) << 2);
            out += "=";
            break;
        }
        c3 = str.charCodeAt(i++);
        out += base64EncodeChars.charAt(c1 >> 2);
        out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
        out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
        out += base64EncodeChars.charAt(c3 & 0x3F);
    }
    return out;
}
/**
 * base64解码
 * @param {Object} str
 */
function base64decode(str){
    var c1, c2, c3, c4;
    var i, len, out;
    len = str.length;
    i = 0;
    out = "";
    while (i < len) {
        /* c1 */
        do {
            c1 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
        }
        while (i < len && c1 == -1);
        if (c1 == -1)
            break;
        /* c2 */
        do {
            c2 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
        }
        while (i < len && c2 == -1);
        if (c2 == -1)
            break;
        out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));
        /* c3 */
        do {
            c3 = str.charCodeAt(i++) & 0xff;
            if (c3 == 61)
                return out;
            c3 = base64DecodeChars[c3];
        }
        while (i < len && c3 == -1);
        if (c3 == -1)
            break;
        out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));
        /* c4 */
        do {
            c4 = str.charCodeAt(i++) & 0xff;
            if (c4 == 61)
                return out;
            c4 = base64DecodeChars[c4];
        }
        while (i < len && c4 == -1);
        if (c4 == -1)
            break;
        out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
    }
    return out;
}