function load_keys(data) {
    console.info(data);
    var data_len = data.length;
    var t_name = "t_keys";
    clear_table(t_name);
    if (data_len == 0) {
        add_row_td(t_name, "暂无密钥");
    }
    for (var i = 0; i < data_len; i++) {
        var data_item = data[i];
        var add_tr = $("<tr></tr>");

        add_tr.append(new_td("app", data_item));
        add_tr.append(new_td("deadline", data_item));
        add_tr.append(new_td("ip_auth", data_item));
        add_tr.append(new_td("user_name", data_item));
        $("#" + t_name).append(add_tr);
    }
}


$(document).ready(function () {
    var query_url = $("#query_url").val();
    my_async_request2(query_url, "POST", {}, load_keys)
});