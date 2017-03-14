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
    for (var i = 0; i < data_len; i++) {
        var server_item = upstream_data["data"][i];
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
        var td_4 = $("<td></td>");
        td_4.append($("<a href='javascript:void(0)' name='link_delete_upstream'>删除</a>"));
        add_tr.append(td_4);
        t.append(add_tr);
    }
    if (op_role == "1") {
        t.find("a[name='link_delete_upstream']").click(function () {
            var current_td = $(this).parent();
            var parent_tr = current_td.parent();
            var current_t = parent_tr.parent().parent();
            var server_item = parent_tr.find("td:first").text();
            var swal_text = server_item;
            swal({
                    title: "确定删除",
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
                        var t_id = current_t.attr("id");
                        var r_url = location.href + t_id.substr(2) + "/";
                        my_async_request2(r_url, "DELETE", {"server_item": server_item}, update_upstream);
                    }
                }
            );
        });
    }
}

function update_upstream(data) {
    $("button[disabled='disabled']").removeAttr("disabled");
    console.info($("button"));
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
    if (str_2_ip(request_data["server_ip"]) <= 0) {
        return;
    }
    var r_url = location.href + btn_parent.attr("id").substr(4) + "/";
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