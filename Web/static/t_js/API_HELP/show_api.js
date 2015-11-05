/**
 * Created by msg on 11/3/15.
 */

function change_care(){
    if ($("#make_care").text() == "关注")
    {
        new_care();
    }
    else if($("#make_care").text() == "取消关注")
    {
        remove_care();
    }
}

function new_care(){
    var api_no = $("#api_no").val();
    $.ajax({
        url: "/dev/api/add/care/",
        method: "POST",
        data:{api_no:api_no},
        success:function(data){
            var json_obj = JSON.parse(data);
            if (json_obj.status == true){
                $("#make_care").text("取消关注");
                $("#api_care_user").append('<span id="mine_care">我</span>');
            }
            else{
                alert(data)
            }
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}

function remove_care(input_no){
    var api_no = $("#api_no").val();
    $.ajax({
        url: "/dev/api/delete/care/" + api_no + "/",
        method: "DELETE",
        success:function(data){
            var json_obj = JSON.parse(data);
            if (json_obj.status == true){
                $("#make_care").text("关注");
                $("#mine_care").remove();
            }
            else{
                alert(data)
            }
        },
        error:function(xhr){
            alert(xhr.statusText);
        }
    });
}
