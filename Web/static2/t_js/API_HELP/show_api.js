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
