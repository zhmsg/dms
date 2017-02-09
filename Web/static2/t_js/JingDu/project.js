/**
 * Created by msg on 2/9/17.
 */

var query_project_ing = new Object({"exec_r": null, "exec_completed": false, "exec_ing": false});

function show_project_info(project_data){
    var pro_len = project_data.length;
    var t_project = $("#t_project_info");
    var keys = ["project_no", "project_name", "description", "date_created", "display_level", "completed", "lastModify"];
    var v_len = [null, 10, 10, 12, null, null, 12, null];
    for(var i=0;i<pro_len;i++){
        var add_tr = $("<tr></tr>");
        for(var j=0;j<keys.length;j++){
            var one_td = new_td(keys[j], project_data[i], v_len[j]);
            add_tr.append(one_td);
        }
        var op_td = $('<td><a name="td_look_partner" href="javascript:void(0)">查看参与者</a></td>');
        add_tr.append(op_td);
        t_project.append(add_tr);
    }

}

function query_project_info(){
    if(query_project_ing.exec_ing == true){
        return;
    }
    query_project_ing.exec_ing = true;
    query_project_ing.exec_completed = false;
    var request_url = "project/";
    my_async_request2(request_url, "GET", null, show_project_info, query_project_ing);
}

$(document).ready(function () {
    $("#btn_last_project").click(query_project_info);
});