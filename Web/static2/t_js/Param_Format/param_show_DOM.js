/**
 * Created by msg on 9/23/16.
 */

function New_TD(key, obj){
    var td = $("<td></td>");
    if(key in obj){
        td.append(obj[key]);
    }
    return td;
}


function Add_TR(param_obj){
    var t = $("#t_params_info");
    var tr_id = 'tr_param_' + param_obj["param"];
    var exist_tr = $("#" + tr_id);
    if(exist_tr.length == 1){
        exist_tr.html("");
        var add_tr = exist_tr;
    }
    else {
        var add_tr = $("<tr id='" + tr_id + "'></tr>");
    }
    t.append(add_tr);

    var keys = ["param", "param_type", "min_len", "max_len", "not_allow", "match_str", "param_desc"];
    for(var i=0;i<keys.length;i++){
        var key = keys[i];
        add_tr.append(New_TD(key, param_obj));
    }

    var op_td = $("<td></td>");
    var up_a = $("<a href='javascript:void' data-toggle='modal' data-target='#div_add_param'>更新</a>");
    up_a.click(click_update);
    op_td.append(up_a);
    op_td.append(" | ");
    var del_a = $("<a href='javascript:void'>删除</a>");
    op_td.append(del_a);
    add_tr.append(op_td);
}