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
    console.info(div_env);
    div_env.find("span").remove();
    var new_div = div_env.clone(true);
    new_div.find("input").val("");

    $("#li_env").append(new_div);

    var all_div_env = $("div[name='div_add_env']");
    var div_len = all_div_env.length;
    for(var i=0;i<div_len;i++){
        var one_div = all_div_env[i];
        var div_nodes = one_div.childNodes;
        var node_len = div_nodes.length;
        for(var j= node_len - 1;j>=0;j--){
            var one_node = div_nodes[j];
            if(one_node.nodeName == "SPAN"){
                one_node.remove();
            }
        }
        var new_span = $('<span class="symbol" onclick="del_env(this);">-</span>');
        new_span.appendTo(one_div);
        if(i == div_len - 1 && i < 4){
            var new_plus_span = $('<span class="symbol" onclick="add_env();">+</span>');
            new_plus_span.appendTo(one_div);
        }
    }

}

function del_env(el)
{
    el.parentNode.remove();
    var all_div_env = $("div[name='div_add_env']");
    var div_len = all_div_env.length;
    if(div_len == 1){
        var one_div = all_div_env[0];
        var div_nodes = one_div.childNodes;
        var node_len = div_nodes.length;
        for(var j=node_len - 1;j>=0;j--){
            var one_node = div_nodes[j];
            if(one_node.nodeName == "SPAN"){
                one_node.remove();
            }
        }
        var new_plus_span = $('<span class="symbol" onclick="add_env();">+</span>');
        new_plus_span.appendTo(one_div);
    }
    else
    {
        for(var i=0;i<div_len;i++){
            var one_div = all_div_env[i];
            var div_nodes = one_div.childNodes;
            var node_len = div_nodes.length;
            for(var j=node_len - 1;j>=0;j--){
                var one_node = div_nodes[j];
                if(one_node.nodeName == "SPAN"){
                    one_node.remove();
                }
            }
            var new_span = $('<span class="symbol" onclick="del_env(this);">-</span>');
            new_span.appendTo(one_div);
            if(i == div_len - 1 && i < 4){
                var new_plus_span = $('<span class="symbol" onclick="add_env();">+</span>');
                new_plus_span.appendTo(one_div);
            }
        }
    }
}

