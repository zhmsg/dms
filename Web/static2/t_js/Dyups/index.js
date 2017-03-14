/**
 * Created by msg on 3/13/17.
 */

function current_upstream(upstream_data) {
    var upstream_name = upstream_data.name;
    var t_id = "t_" + upstream_name;
    var t = $("#" + t_id);
    var op_role = t.attr("op_role");
    if (t.length <= 0) {
        return;
    }
    clear_table(t_id);
    var data_len = upstream_data["data"].length;
    var delete_op = "<a href='javascript:void(0)' name='link_op_upstream'>删除</a>";
    var add_op = "<a href='javascript:void(0)' name='link_op_upstream'>添加</a>";
    var set_save = "<a href='javascript:void(0)' name='link_op_server'>设为常用</a>";
    var remove_save = "<a href='javascript:void(0)' name='link_op_server'>移除常用</a>";
    for (var i = 0; i < data_len; i++) {
        var server = upstream_data["data"][i];
        var server_item = server["server_item"];
        var add_tr = $("<tr></tr>");
        var td_1 = $("<td></td>");
        td_1.text(server_item);
        add_tr.append(td_1);
        var ip_port = server_item.substr(7).split(":");
        var td_2 = $("<td></td>");
        td_2.text(ip_port[0]);
        add_tr.append(td_2);
        var td_3 = $("<td></td>");
        td_3.text(ip_port[1]);
        add_tr.append(td_3);
        add_tr.append(new_td("status_desc", server));
        var td_op = $("<td></td>");
        if (server["status"] == 1) {
            td_op.append($(delete_op));
        }
        else {
            td_op.append($(add_op));
        }
        td_op.append(" | ");
        if (server.hasOwnProperty("adder")) {
            td_op.append($(remove_save));
        }
        else {
            td_op.append($(set_save));
        }
        add_tr.append(td_op);
        t.append(add_tr);
    }
    if (op_role == "1") {
        t.find("a[name^='link_op_']").click(function () {
            var current_td = $(this).parent();
            var parent_tr = current_td.parent();
            var current_t = parent_tr.parent().parent();
            var upstream_name = current_t.attr("id").substr(2);
            var server_ip = parent_tr.find("td:eq(1)").text();
            var server_port = parent_tr.find("td:eq(2)").text();
            var link_name = $(this).attr("name");
            var r_url = $("#" + link_name.substr(5) + "_url").val();
            var r_data = {"upstream_name": upstream_name, "server_ip": server_ip, "server_port": server_port};
            var r_method = "POST";
            if ($(this).text() == "移除常用" || $(this).text() == "删除") {
                r_method = "DELETE";
            }
            my_async_request2(r_url, r_method, r_data, update_upstream);
        });
    }
}

function update_upstream(data) {
    $("button[disabled='disabled']").removeAttr("disabled");
    if (data == "success") {
        location.reload();
    }
    else {
        sweetAlert(data);
    }
}

function submit_add() {
    var current_btn = $(this);
    var btn_parent = current_btn.parent();
    var all_input = btn_parent.find("input");
    var request_data = new Object();
    for (var i = 0; i < all_input.length; i++) {
        var current_input = $(all_input[i]);
        var name = current_input.attr("name");
        var value = current_input.val();
        request_data[name] = value;
    }
    request_data["upstream_name"] = btn_parent.attr("id").substr(4);
    if (str_2_ip(request_data["server_ip"]) <= 0) {
        return;
    }
    var r_url = $("#op_upstream_url").val();
    if (request_data["server_ip"].match(/^(192\.168\.120\.|127\.0\.0\.)\d{1,3}$/)) {
        my_async_request2(r_url, "POST", request_data, update_upstream);
        current_btn.attr("disabled", "disabled");
    } else {
        var swal_text = "确定提交" + request_data["server_ip"] + "\n最好以192.168.120.或者127.0.0.开头";
        swal({
                title: "确定提交",
                text: swal_text,
                type: "info",
                showCancelButton: true,
                confirmButtonColor: '#DD6B55',
                confirmButtonText: '提交',
                cancelButtonText: "取消",
                closeOnConfirm: true,
                closeOnCancel: true
            },
            function (isConfirm) {
                if (isConfirm) {
                    my_async_request2(r_url, "POST", request_data, update_upstream);
                    current_btn.attr("disabled", "disabled");
                }
            }
        );
    }
}

$(document).ready(function () {
    $("table").each(function () {
        var current_t = $(this);
        var t_id = current_t.attr("id");
        add_row_td(t_id, "查询中");
        var request_url = location.href + t_id.substr(2) + "/";
        my_async_request2(request_url, "GET", null, current_upstream);
    });
    $("div[name='div_new_server']").each(function () {
        var current_div = $(this);
        var role = current_div.find("input:first").val();
        if (role <= 0) {
            current_div.find("button").text("暂无权限");
        }
        else {
            current_div.find("button").click(submit_add);
            $("#t_" + current_div.attr("id").substr(4)).attr("op_role", "1");
        }
    });
    $("input[name='server_ip']").keyup(function () {
        $(this).val(format_ip($(this).val()));
    });
});