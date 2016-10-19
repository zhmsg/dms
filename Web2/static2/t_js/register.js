/**
 * Created by msg on 1/11/16.
 */

function check_user_name_success(data){
    if(data.status == true){
        $("#check_result").text("可以添加注册");
        $("#user_name").val(data.message);
    }
    else{
        $("#check_result").text(data.message);
    }
}

function check_user_name(){
    var user_name = $("#user_name").val();
    var check_url = $("#check_url").val();

    my_async_request(check_url, "POST", {check_name:user_name}, check_user_name_success);
}