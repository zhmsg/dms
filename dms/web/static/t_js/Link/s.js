/**
 * Created by msg on 17-7-6.
 */


function op_link(is_query) {
    var sl_url = $("#link_op_s").attr("sl_url") + "/";
    var r_data = new Object();
    if (is_query != null) {
        r_data["is_query"] = true;
    }
    r_data["link"] = location.href;
    r_data["remark"] = document.title;
    console.info('0----');
    console.info(sl_url);
    my_async_request2(sl_url, "POST", r_data, handler2);
}

function handler2(data) {
    console.info(data);
    if (data == null) {
        $("#link_op_s").show();
        $("#link_op_s").text("生成短链");
    }
    else {
        $("#link_op_s").attr("s", data);
        $("#link_op_s").show();
        var title = location.protocol + "//" + location.host + $("#link_op_s").attr("sl_url") + "/" + data + "/";
        console.info(title);
        $("#link_op_s").attr("title", title);
        $("#link_op_s").text("复制短链");
    }
}

function create_link() {
    var s = $("#link_op_s").attr("s");
    console.info(s);
    if (s != null) {
        var s_link = location.protocol + "//" + location.host + $("#link_op_s").attr("sl_url") + "/" + s + "/";
        copy_text(s_link);
    }
    else {
        op_link();
    }


}

$(document).ready(function () {
    if ($("#current_user_name").length > 0) {
        var current_url = location.pathname;
        var path = location.href.substr(location.protocol.length + 2 + location.host.length);
        if (path.length > 32 && current_url.length > 2) {
            op_link(true);
            $("#link_op_s").click(create_link);
        }
    }
});