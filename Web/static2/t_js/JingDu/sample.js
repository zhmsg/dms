/**
 * Created by msg on 2/9/17.
 */

var query_sample_ing = new Object({"exec_r": null, "exec_completed": false, "exec_ing": false});
var query_si_ing = new Object({"exec_r": null, "exec_completed": false, "exec_ing": false});
var query_su_ing = new Object({"exec_r": null, "exec_completed": false, "exec_ing": false});

function click_look_owner(){
    var current_a = $(this);
    var tr_parent = current_a.parent().parent();
    var td_sample_no = tr_parent.find("td[name='td_sample_no']");
    if(td_sample_no.text() == $("#su_no_name").val()){
        return;
    }
    $("#su_no_name").val(td_sample_no.text());
    $("#btn_sample_user").click();
}

function click_look_sample(){
    var current_a = $(this);
    var tr_parent = current_a.parent().parent();
    var td_sample_no = tr_parent.find("td[name='td_sample_no']");
    if(td_sample_no.text() == $("#s_no").val()){
        return;
    }
    $("#s_no").val(td_sample_no.text());
    $("#btn_last_sample").click();
}

function click_look_stage(){
    if(query_si_ing.exec_ing == true){
        return;
    }
    query_si_ing.exec_ing = true;
    query_si_ing.exec_completed = false;
    var current_a = $(this);
    current_a.text("查询中");
    var tr_parent = current_a.parent().parent();
    var td_sample_no = tr_parent.find("td[name='td_sample_no']");
    tr_parent.attr("id", "tr_sample_" + td_sample_no.text());
    var request_url = "sample/info/?sample_no=" + td_sample_no.text();
    my_async_request2(request_url, "GET", null, show_stage, query_si_ing)
}

function show_stage(sample_info){
    var si_len = sample_info.length;
    for(var i=0;i<si_len;i++){
        var info_item = sample_info[i];
        var sample_no = info_item.sample_no;
        var td_stage = $("#tr_sample_" + sample_no).find("td[name='td_look_stage']");
        var stage_text = "";
        console.info(info_item.stage);
        switch(info_item.stage)
        {
            case 3:
                stage_text = "<a>检查突变</a>";
                break;
            default:
                stage_text = info_item.stage;
        }
        td_stage.text(info_item.stage);
    }
}

function show_sample_info(sample_data){
    var sam_len = sample_data.length;
    clear_table("t_sys_sample");
    var t_sample = $("#t_sys_sample");
    var keys = ["sample_no", "sample_id", "patient_no", "date_created", "display_level", "portal"];
    for(var i=0;i<sam_len;i++){
        var add_tr = $("<tr></tr>");
        for(var j=0;j<keys.length;j++){
            var one_td = new_td(keys[j], sample_data[i]);
            add_tr.append(one_td);
        }
        var stage_td = $('<td name="td_look_stage"><a name="link_look_stage" href="javascript:void(0)">查看状态</a></td>');
        add_tr.append(stage_td);
        var op_td = $('<td name="td_look_owner"><a name="link_look_owner" href="javascript:void(0)">拥有者</a></td>');
        add_tr.append(op_td);
        t_sample.append(add_tr);
    }
    $("td[name='td_display_level']:visible").each(function(){
        var current_td = $(this);
        if(current_td.text() == "0"){
            current_td.text("公开");
        }
        else{
            current_td.text("私有");
        }
    });
    $("a[name='link_look_stage']:visible").each(function(){
       var current_td = $(this);
        current_td.unbind("click");
        current_td.click(click_look_stage);
    });
    $("a[name='link_look_owner']").each(function(){
        var current_td = $(this);
        current_td.unbind("click");
        current_td.click(click_look_owner);
    });
}

function query_sys_sample(){
    if(query_sample_ing.exec_ing == true){
        return;
    }
    query_sample_ing.exec_ing = true;
    query_sample_ing.exec_completed = false;
    var input_key = $("#s_no").val();
    $("#lab_s_error_key").hide();
    var m_sample_no = input_key.match("^\\d{1,10}$");
    var request_url = "sample/";
    if(m_sample_no != null){
        request_url += "?sample_no=" + m_sample_no[0];
    }
    my_async_request2(request_url, "GET", null, show_sample_info, query_sample_ing);
}

function show_sample_user(su_data){
    var su_len = su_data.length;
    clear_table("t_sample_user");
    var t_sample = $("#t_sample_user");
    var keys = ["sample_no", "account", "role"];
    for(var i=0;i<su_len;i++){
        var add_tr = $("<tr></tr>");
        for(var j=0;j<keys.length;j++){
            var one_td = new_td(keys[j], su_data[i]);
            add_tr.append(one_td);
        }
        var op_td = $('<td><a name="link_look_sample" href="javascript:void(0)">样本信息</a>');
        add_tr.append(op_td);
        t_sample.append(add_tr);
    }
    $("td[name='td_role']:visible").each(function(){
        var current_td = $(this);
        var role_desc = "";
        switch(current_td.text())
        {
            case "0":
                role_desc = "创建者";
                break;
                break;
            default:
                role_desc = "无效数据";
        }
        current_td.text(current_td.text() + "|" + role_desc);
    });
    $("a[name='link_look_sample']:visible").each(function(){
        var current_td = $(this);
        current_td.unbind("click");
        current_td.click(click_look_sample);
    });
}

function query_sample_user(){
    if(query_su_ing.exec_ing == true){
        console.info("查询中");
        return;
    }
    query_su_ing.exec_ing = true;
    query_su_ing.exec_completed = false;
    var input_key = $("#su_no_name").val();
    $("#lab_su_error_key").hide();
    var m_sample_no = input_key.match("^\\d{1,10}$");
    if(m_sample_no != null){
        var sample_no = m_sample_no[0];
        var request_url = "sample/user/?sample_no=" + sample_no;
        my_async_request2(request_url, "GET", null, show_sample_user, query_su_ing);
        return;
    }
    var m_account = input_key.match("^[a-zA-Z]\\w{4,19}$");
    if(m_account != null){
        var account = m_account[0];
        var request_url = "sample/user/?account=" + account;
        my_async_request2(request_url, "GET", null, show_sample_user, query_su_ing);
        return;
    }
    query_su_ing.exec_ing = false;
    $("#lab_su_error_key").show();
}

$(document).ready(function () {
    $("#btn_last_sample").click(query_sys_sample);
    $("#btn_sample_user").click(query_sample_user);
});