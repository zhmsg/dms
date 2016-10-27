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