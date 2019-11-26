/**
 * Created by msg on 1/11/16.
 */

function check_user_name_success(data){
    if(data.data.result == true){
        $("#check_result").text("已被注册");
    }
    else{
        $("#check_result").text("可以注册");
    }
}

function check_user_name(){
    var user_name = $("#user_name").val();
    if(user_name.length < 3){
        return false;
    }
    var check_url = $("#check_url").val();

    my_async_request(check_url, "POST", {check_name:user_name}, check_user_name_success);
}