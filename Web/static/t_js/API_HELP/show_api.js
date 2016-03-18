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

function new_care(new_url){
    var api_no = $("#api_no").val();
    $.ajax({
        url: new_url,
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

function remove_care(remove_url){
    var api_no = $("#api_no").val();
    $.ajax({
        url: remove_url,
        method: "DELETE",
        data:{api_no:api_no},
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
