/**
 * Created by msg on 5/26/16.
 */

function add_option(select_id, value, text, title){
    if(title == null){
        title = text;
    }
    var option = "<option value='{value}' title='{title}'>{text}</option>";
    var option_item = option.replace("{value}", value).replace("{text}", text).replace("{title}", title);
    $("#" + select_id).append(option_item);
}

function query_option(select_id, v, query_t){
    if(query_t == null){
        query_t = "value";
    }
    if (query_t != "text") {
        var query_option = $("#" + select_id).find("[" + query_t + "='" + v + "']");
    } else {
        var each_option = $("#" + select_id).find("option");
        var query_option = [];
        var fix_count = 0;
        for (var i = 0; i < each_option.length; i++) {
            var current_option = $(each_option[i]);
            if (current_option.text() == v) {
                query_option[fix_count] = current_option;
                fix_count++;
            }
        }
    }
    return query_option;
}

function new_td(key, obj, max_len, editable) {
    var td = $("<td></td>");
    if(key in obj){
        var td_text = obj[key] + "";
        if(max_len != null){
            if(td_text.length > max_len){
                td.attr("title", td_text);
                td_text = td_text.substr(0, max_len - 2) + ".."
            }
        }
        td.attr("name", "td_" + key);
        if (editable != null && editable == true) {
            var e = $("<input />");
            e.css("border", 0);
            e.css("background-color", "transparent");
            e.val(td_text);
            td.append(e);
        }
        else {
            td.append(td_text);
        }
    }
    return td;
}

function clear_table(table_id){
    $("#" + table_id + " tr").not(":first").remove();
}

function add_row_td(t_id, content, col_len)
{
    var t =$("#" + t_id);
    var add_tr = $("<tr></tr>");
    var add_td = $("<td></td>");
    add_td.text(content);
    if(col_len == null){
        var th_len = t.find("th").length;
        if(th_len > 0)
            col_len = th_len;
        else
            col_len = 1;
    }
    add_td.css({"text-align": "center"});
    add_td.attr("colSpan", col_len);
    add_tr.append(add_td);
    t.append(add_tr);
}

function query_table(t_id, key){
    var trs = $("#" + t_id + " tr").not(":first");
    var tr_len = trs.length;
    for(var i=0;i<tr_len;i++){
        var tr_item = $(trs[i]);
        var tr_tds = tr_item.find("td");
        var td_len = tr_tds.length;
        var is_show = false;
        for(var j=0;j<td_len;j++){
            var td_item = $(tr_tds[j]);
            if(td_item.text().indexOf(key) >= 0){
                is_show = true;
                break;
            }
        }
        if(is_show == true){
            tr_item.show();
        }
        else{
            tr_item.hide();
        }
    }
}