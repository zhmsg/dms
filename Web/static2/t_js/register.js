/**
 * Created by msg on 1/11/16.
 */

function check_user_name(){
    var user_name = $("#user_name").val();
    var check_url = $("#check_url").val();
    $.ajax({
        url: check_url,
        method: "POST",
        data:{check_name:user_name},
        success:function(data){
            if(data.status == true){
                $("#check_result").text("可以添加注册");
                $("#user_name").val(data.message);
            }
            else{
                $("#check_result").text(data.message);
            }
        },
        error:function(xhr){
            $("#check_result").text(xhr.statusText);
        }
    });
}