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
            $("#" + data_item.id).next().remove();
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
        sessionStorage.setItem("jy_dms_distKey_" + data_item.id, JSON.stringify(data_item));
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
        detail_tr.attr("id", "tr_detail_" + data_item.id);
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
        detail_td.append($('<a href="javascript:void(0)" onclick="switch_to_detail(\'' + data_item.id + '\')">More</a>'));
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

function receive_secret(data)
{
    console.info(data);
    var li_id = data.id + "__" + data.key;
    console.info(li_id);
    $("#" + li_id).find("[name='link_receive']").hide();
    $("#" + li_id).find("[name='link_copy']").show();
    var ss_key = "jy_dms_distKey_" + data.id;
    var data_item = JSON.parse(sessionStorage.getItem(ss_key));
    data_item[data.key] = data.value;
    sessionStorage.setItem(ss_key, JSON.stringify(data_item));
}

function switch_to_detail(id)
{
    var data_item = JSON.parse(sessionStorage.getItem("jy_dms_distKey_" + id));
    console.info(data_item);
    $("#detail_key_id").val(data_item.id);
    $("#app2").val(data_item.app);
    $("#deadline").val(data_item.deadline);
    $("#div_key_all li:not(:last)").remove();
    var first_li = $("#div_key_all li:first");
    first_li.show();
    for(var key in data_item){
        if(["user_name", "id", "ip_auth", "deadline", "app", "insert_time", "remark"].indexOf(key) >= 0){
            continue;
        }
        var c_li = first_li.clone(true);
        c_li.attr("id", id + "_" + key);
        if(key[0] == "_"){
            c_li.find("input:first").val(key.substr(1));
            c_li.find("[name='link_copy']").hide();
            c_li.find("[name='link_receive']").show();
            c_li.find("[name='link_receive']").click(function(){
                var key_id = $("#detail_key_id").val();
                var key = $(this).parent().find("input:first").val();
                my_async_request2("/dist/key/query/secret/", "POST", {"id": key_id, "key": key}, receive_secret);
            });
        }
        else{
            c_li.find("input:first").val(key);
        }
        c_li.find("[name='link_copy']").click(function(){
            var ss_key = "jy_dms_distKey_" + $("#detail_key_id").val();
            var item = JSON.parse(sessionStorage.getItem(ss_key));
            copy_text(item[$(this).parent().find("input:first").val()]);
        });
        c_li.find("input:last").val(data_item[key]);
        first_li.before(c_li);
    }
    first_li.hide();
    var update_link = $('<a class="status_move">更新</a>');
    update_link.click(function(){
        var parent_li = $(this).parent();
        var current_action = $(this).text();
        if(current_action == "更新"){
            parent_li.find("input:eq(1)").removeAttr("readonly");
            $(this).text("保存");
        }
        else{
            var value_input = parent_li.find("input:eq(1)");
            value_input.attr("readonly", "readonly");
            var parent_id = parent_li.attr("id");
            var index = parent_id.indexOf("_");
            var doc_id = parent_id.substring(0, index);
            var doc_key = parent_id.substring(index + 1, parent_id.length);
            var doc_value = value_input.val();
            var data = {"doc_id": doc_id, "doc_key": doc_key, "doc_value": doc_value};
            var value_url = $("#value_url").val();
            my_async_request2(value_url, "PUT", data);
            $(this).text("更新");
        }
    });
    $("#div_key_all li:not(:last)").append(update_link);
    $("#div_key_all input").attr("readonly", "readonly");
    $("#ul_menu li:eq(2) a").tab('show');
}

$(document).ready(function () {
    var query_url = $("#query_url").val();
    my_async_request2(query_url, "POST", {}, load_keys)
});