/**
 * Created by msg on 3/13/17.
 */

function current_upstream(upstream_data) {
    var upstream_name = upstream_data.name;
    var t_id = "t_" + upstream_name;
    var t = $("#" + t_id);
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
    $("a[name='link_delete_upstream']").click(function () {
        var current_td = $(this).parent();
        var parent_tr = current_td.parent();
        var current_t = parent_tr.parent().parent();
        var server_item = parent_tr.find("td:first").text();
        console.info(server_item);
        console.info($(current_t));
        var t_id = current_t.attr("id");
        var r_url = location.href + t_id.substr(2, 3) + "/";
        my_async_request2(r_url, "DELETE", {"server_item": server_item}, update_upstream);
    });
}

function update_upstream(data) {
    if (data == "success") {
        location.reload();
    }
    else {
        sweetAlert(data);
    }
}

$(document).ready(function () {
    add_row_td("t_webcluster", "查询中");
    add_row_td("t_apicluster", "查询中");
    var request_url = location.href + "web/";
    my_async_request2(request_url, "GET", null, current_upstream);
    request_url = location.href + "api/";
    my_async_request2(request_url, "GET", null, current_upstream);
    $("button[name='btn_add_upstream']").click(function () {
        var current_btn = $(this);
        var btn_parent = current_btn.parent();
        var all_input = btn_parent.find("input");
        var request_data = new Object();
        for (var i = 0; i < all_input.length; i++) {
            var current_input = $(all_input[i]);
            var name = current_input.attr("name");
            console.info(name);
            var value = current_input.val();
            request_data[name] = value;
        }
        var r_url = location.href + request_data["name"] + "/";
        my_async_request2(r_url, "POST", request_data, update_upstream);
        console.info(request_data);
    });
});