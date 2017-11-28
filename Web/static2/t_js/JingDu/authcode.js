/**
 * Created by msg on 17-11-28.
 */

function auth_code_data(data) {
    if(data == null) {
        $("#lab_s_error_code").hide();
        var url = $("#auth_code_url").val();
        var auth_code = $("#authcode").val();
        var code_type = $("#code_type").val();
        my_async_request2(url, "POST", {"auth_code": auth_code, "code_type": code_type}, auth_code_data);
    }
    console.info(data);
}

$(document).ready(function () {
    $("#btn_new_authcode").click(function () {
        auth_code_data();
    });
});