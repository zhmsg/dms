/**
 * Created by msg on 11/3/15.
 */

function change_care(){
    var change_url = $("#care_url").val();
    if ($("#make_care").text() == "关注")
    {
        new_care(change_url);
    }
    else if($("#make_care").text() == "取消关注")
    {
        remove_care(change_url);
    }
}

function change_care_success(data){
    if ($("#make_care").text() == "关注")
    {
        $("#make_care").text("取消关注");
        $("#api_care_user").append('<span id="mine_care">我</span>');
    }
    else if($("#make_care").text() == "取消关注")
    {
        $("#make_care").text("关注");
        $("#mine_care").remove();
    }
}

function new_care(new_url){
    var api_no = $("#api_no").val();
    my_async_request(new_url, "POST", {api_no: api_no}, change_care_success);
}

function remove_care(remove_url){
    var api_no = $("#api_no").val();
    my_async_request(remove_url, "DELETE", {api_no: api_no}, change_care_success);
}

$(function() {
    var current_user_name = $("#current_user_name").val();
    var care_info = JSON.parse($("#lab_care_info").text());
    for(var i=0;i<care_info.length;i++){
        if(care_info[i]["user_name"] == current_user_name){
            $("#api_care_user").append('<span id="mine_care">我</span>');
            if(care_info[i]["level"] == 0){ // 关注level为0 为API创建者不可取消关注
                $("#make_care").hide();
                $("#btn_del_api").show();
                $("#btn_del_api").click(function(){my_request($("#del_api_url").val(), "DELETE")});
            }
            else {
                $("#make_care").text("取消关注");
            }
        }
        else {
            $("#api_care_user").append('<span>' + care_info[i]["nick_name"] + '</span>');
        }
    }

    var current_user_role = parseInt($("#current_user_role").val());
    var role_value = JSON.parse($("#role_value").text());
    if(bit_and(current_user_role, role_value["api_new"])){
        $("#a_update_api").attr("href", location.href + "&update=");
        $("div[id^='div_api_new_']").show();
    }

    $("#link_copy_location").click(function(){
        copy_text(location.href);
    });
});