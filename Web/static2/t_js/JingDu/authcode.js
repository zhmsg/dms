/**
 * Created by msg on 17-11-28.
 */

function auth_code_data(data) {
    if(data == null) {
        $("#lab_s_error_code").hide();
        var url = $("#auth_code_url").val();
        var auth_code = $("#authcode").val();
        var code_type = $("#code_type").val();
        var r_data = {"code_type": code_type};
        if(auth_code.length != 0 && auth_code.length < 4){
            $("#lab_s_error_code").show();
            return false;
        }
        else if(auth_code.length >= 4){
            r_data["auth_code"] = auth_code;
        }
        my_async_request2(url, "POST", r_data, auth_code_data);
    }
    var t_id = "t_authcode_list";
    console.info(data);
    var keys = ["code", "code_type", "account", "start_time", "end_time", "avail_times", "insert_time"];
        var key_len = keys.length;
    var add_tr = $("<tr></tr>");
    for (var j = 0; j < key_len; j++) {
        add_tr.append(new_td(keys[j], data));
    }
    $("#" + t_id).append(add_tr);
}

$(document).ready(function () {
    $("#btn_new_authcode").click(function () {
        auth_code_data();
    });
});