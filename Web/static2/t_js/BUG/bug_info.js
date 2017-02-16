/**
 * Created by msg on 2/16/17.
 */

function submit_bug_reason(){
    var bug_reason = $(this).prevAll("textarea").val();
    if(bug_reason.length <= 0){
        return;
    }
    var url_bug_reason = $("#url_bug_reason").val();
    var button_text = $(this).text();
    var request_method = "POST";
    if(button_text == "更新"){
        request_method = "PUT";
    }
    my_async_request2(url_bug_reason, request_method, {"bug_reason": bug_reason}, handle_bug_reason);
}


function handle_bug_reason(bug_reasons){
    console.info(bug_reasons);
    var br_len = bug_reasons.length;
    if(br_len > 0){
        for(var i=0;i<br_len;i++){
            var reason_item = bug_reasons[i];
            console.info(reason_item);
            if(reason_item["submitter"] == $("#current_user_name").val()){
                $("#div_add_reason").find("textarea").val(reason_item["reason"]);
                $("#div_add_reason").find("button").text("更新");
                break;
            }
        }
    }
    var submit_button = $("#div_add_reason").find("button");
    submit_button.unbind("click");
    submit_button.click(submit_bug_reason);
}

function handler_bug_links(link_users)
{
    var lu_len = link_users.length;
    for(var i=0;i<lu_len;i++){
        var user_item = link_users[i];
        if(user_item["type"] == 2){
            if(user_item["user_name"] == $("#current_user_name").val()){
                var url_bug_reason = $("#url_bug_reason").val();
                my_async_request2(url_bug_reason, "GET", null, handle_bug_reason);
                $("#div_add_reason").show();
            }
        }
    }
}


$(document).ready(function () {
    var url_link_user = $("#url_link_user").val();
    my_async_request2(url_link_user, "GET", null, handler_bug_links)
});