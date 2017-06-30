/**
 * Created by msg on 17-6-30.
 */

function list_barcode(data) {
    var t_id = "t_barcode_list";
    if (data != null) {
        console.info(data);
        clear_table(t_id);
        var d_len = data.length;
        var keys = ["barcode_num", "app_list", "app_id", "account", "sample_no", "stage", "auto_gen", "version"];
        var key_len = keys.length;
        for (var i = 0; i < d_len; i++) {
            var add_tr = $("<tr></tr>");
            for (var j = 0; j < key_len; j++) {
                add_tr.append(new_td(keys[j], data[i]));
            }
            $("#" + t_id).append(add_tr);
        }
        if (d_len == 0) {
            add_row_td(t_id, "未查找到");
        }
    }
    else {
        var query_url = $("#barcode_url").val();
        var barcode_num = $("#barcode_num").val();
        if (barcode_num.length <= 0) {
            return false;
        }
        console.info(query_url);
        my_async_request2(query_url, "GET", {"barcode_num": barcode_num}, list_barcode);
    }
}

$(document).ready(function () {
    $("#btn_query_barcode").click(function () {
        list_barcode();
    });
});