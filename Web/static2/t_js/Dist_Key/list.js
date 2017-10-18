function load_keys(data) {
    var data_len = data.length;
    var t_name = "#t_keys";
    //clear_table(t_name);
    if (data_len == 0) {
        add_row_td(t_name, "暂无密钥");
    }
    var col_len = 6;
    var ct = get_timestamp() / 1000;
    var current_user = $("#current_user_name").val();
    for (var i = 0; i < data_len; i++) {
        var data_item = data[i];
        if("deleted" in data_item){
            $("#" + data_item.id).remove();
            continue;
        }
        var left_days = (data_item["deadline"] - ct) / 24 / 60 / 60;
        data_item["deadline"] = timestamp_2_datetime(data_item["deadline"]);
        var add_tr = $("<tr></tr>");
        if($("#" + data_item.id).length > 0){
            add_tr.insertBefore($("#" + data_item.id));
            $("#" + data_item.id).next().remove();
            $("#" + data_item.id).remove();
        }
        else{
            $(t_name).append(add_tr);
        }
        add_tr.attr("id", data_item.id);
        add_tr.append(new_td("app", data_item));
        add_tr.append(new_td("deadline", data_item));
        add_tr.append(new_td("ip_auth", data_item));
        add_tr.append(new_td("user_name", data_item));
        add_tr.append(new_td("remark", data_item));
        var op_td = $("<td></td>");
        op_td.append($("<a name='op_look' href='javascript:void(0)'>查看</a>"));
        if(data_item["ip_auth"] == true && current_user == data_item["user_name"]) {
            if(left_days <= 10) {
                op_td.append(" | ");
                op_td.append($("<a name='update_deadline' href='javascript:void(0)'>延长到期</a>"));
            }
            if(left_days >= 1) {
                op_td.append(" | ");
                op_td.append($("<a name='update_deadline' href='javascript:void(0)'>提前到期</a>"));
            }
            if(left_days <= 0){
                op_td.append(" | ");
                op_td.append($("<a name='op_delete' href='javascript:void(0)'>删除</a>"));
            }
        }
        add_tr.append(op_td);

        var detail_tr = $("<tr name='tr_extend' class='display_none'></tr>");
        var detail_td = $("<td></td>");
        detail_td.css({"text-align": "center"});
        detail_td.attr("colSpan", col_len);
        for(var key in data_item){
            if(["user_name", "id", "ip_auth", "deadline", "app", "insert_time", "remark"].indexOf(key) >= 0){
                continue;
            }
            if(key[0] == "_"){
                detail_td.append(key.substr(1));
            }
            else {
                detail_td.append(key);
            }
            detail_td.append(":");
            detail_td.append(data_item[key]);
            detail_td.append($("<br></br>"));
        }
        detail_tr.append(detail_td);

        detail_tr.insertAfter(add_tr);
    }
    $("a[name='op_look']").click(function(){
        var parent_tr = $(this).parent().parent();
        $("tr[name='tr_extend']").hide();
        if($(this).text() == "查看") {
            parent_tr.next().show();
            $("a[name='op_look']").text("查看");
            $(this).text("隐藏");
        }
        else{
            $(this).text("查看");
        }

    });
    $("a[name='op_delete']").click(function(){
        var parent_tr = $(this).parent().parent();
        var current_id = parent_tr.attr("id");
        var data = {"id": current_id};
        my_async_request2(location.href, "DELETE", data, load_keys);
    });
    $("a[name='update_deadline']").click(function(){
        var parent_tr = $(this).parent().parent();
        var current_id = parent_tr.attr("id");
        var data = {"id": current_id};
        if($(this).text() == "延长到期"){
            data["offset"] = 10 * 24 * 60 * 60;
        }
        else{
            data["deadline"] = get_timestamp2() + 24 * 60 * 60;
        }
        my_async_request2(location.href, "PUT", data, load_keys);

    });
}


$(document).ready(function () {
    var query_url = $("#query_url").val();
    my_async_request2(query_url, "POST", {}, load_keys)
});