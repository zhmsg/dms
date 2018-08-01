/**
 * Created by msg on 17-11-28.
 */

var c_vm = null;

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
    else {
        c_vm.codes.push(data);
    }
}

$(document).ready(function () {
    $("#btn_new_authcode").click(function () {
        auth_code_data();
    });
    c_vm = new Vue({
        el: "#t_authcode_list",
        data: {
            codes: []
        }
    });
});