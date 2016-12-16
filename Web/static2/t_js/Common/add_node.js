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

function new_td(key, obj){
    var td = $("<td></td>");
    if(key in obj){
        td.append(obj[key]);
    }
    return td;
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