/**
 * Created by msg on 3/18/16.
 */


function change_care(module_no){
    if ($("#make_care").text() == "关注")
    {
        new_care(module_no);
    }
    else if($("#make_care").text() == "取消关注")
    {
        remove_care(module_no);
    }
}

function new_care(module_no){
    var change_url = $("#care_url").val();
    $.ajax({
        url: change_url,
        method: "POST",
        data:{module_no:module_no},
        success:function(data){
            var json_obj = JSON.parse(data);
            if (json_obj.status == true){
                $("#make_care").text("取消关注");
                $("#module_care_user").append('<span id="mine_care">我</span>');
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

function remove_care(module_no){
    var change_url = $("#care_url").val();
    $.ajax({
        url: change_url,
        method: "DELETE",
        data:{module_no:module_no},
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

function add_env(){
    var div_env = $("div[name='div_add_env']:eq(0)");
    var all_div_env = $("div[name='div_add_env']");
    div_env.find("span").remove();
    div_env.append('<span class="symbol">-</span>');
    var new_div = div_env.clone(true);
    new_div.find("input").val("");
    if(all_div_env.length < 4) {
        new_div.append('<span class="symbol" onclick="add_env();">+</span>');
    }
    $("#li_env").append(new_div);
    //var all_div_env = $("div[name='div_add_env']");
    for(var i=0;i<all_div_env.length;i++){
        all_div_env[i];
    }

}

