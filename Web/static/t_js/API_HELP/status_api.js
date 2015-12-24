/**
 * Created by msg on 12/24/15.
 */

var fun_info;
function get_module_info() {
    var request_url = $("#fun_info_url").val();
    console.info(request_url);
    $.ajax({
        url: request_url,
        method: "GET",
        success: function (data) {
            alert(data);
            fun_info = data;
        },
        error: function (xhr) {
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            console.info(xhr);
        }
    });
}

function set_service_id(){

}