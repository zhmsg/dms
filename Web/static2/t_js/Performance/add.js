
var score = 0;
var weighted_score = 0;


function load_modules(data){
    var data_len = data.length;
    for(var i=0;i<data_len;i++){
        var d_item = data[i];
        var v = d_item["module_no"] + "|" + d_item["score"] + "|" + d_item["weighted_score"];
        add_option("modules", v, d_item["module_name"]);
    }
    $("#modules").change();
}

function load_users(data){
    var data_len = data.length;
    for(var i=0; i<data_len;i++){
        var u_item = data[i];
        add_option($("li[name='li_members'] select"), u_item["user_name"], u_item["nick_name"]);
    }
}

function reload_score(){
    var lis = $("li[name='li_members']");
    var lis_len = lis.length;
    for(var i=0; i<lis_len; i++){
        var elem = $(lis[i]);
        var all_input = elem.find("input");
        if($(all_input[1]).is(":checked")){
            $(all_input[0]).val(weighted_score);
        }
        else{
            $(all_input[0]).val(score);
        }
    }
}

function f()
{
    var lis = $("li[name='li_members']");
    var lis_len = lis.length;
    var members = new Array();
    for(var i=0; i<lis_len; i++){
        members[i] = $(lis[i]).find("select").val();
    }
    for(var i=0; i<lis_len; i++){
        var options = $(lis[i]).find("select option");
        var options_len = options.length;
        for(var j=0; j<options_len; j++){
            var option_item = $(options[j]);
            option_item.show();
            var option_value = option_item.val();
            for(var k=0; k<lis_len; k++){
                if(option_value == members[k] && k != i){
                    option_item.hide();
                }
            }
        }
    }
}

function new_performance()
{
    var module = parseInt($("#modules").val().split("|")[0]);
    var name = $("#name").val();
    var detail_info = $("#detail_info").val();
    var start_time = $("#start_time").val();
    var end_time = $("#end_time").val();
    var data = {"module": module, "name": name, "detail_info": detail_info, "start_time": start_time,
        "end_time": end_time, "members": new Array()};
    var members_elem = $("li[name='li_members']");
    var mem_num = members_elem.length;
    for(var i=0; i<mem_num; i++){
        var mem_elem = $(members_elem[i]);
        var user_name = mem_elem.find("select").val();
        var is_weighted = $(mem_elem.find("input:eq(1)")).is(":checked");
        var mem_item = {"user_name": user_name, "is_weighted": is_weighted};
        data.members[i] = mem_item;

    }
    console.info(data);
    my_async_request2(location.href, "POST", data);
}

$(document).ready(function () {
    my_async_request2($("#module_url").val(), "GET", null, load_modules);
    my_async_request2($("#list_user_url").val(), "GET", null, load_users);
    $("a[name='link_add_input']").click(function(){
        var p_li = $(this.parentNode);
        p_li.find("select option:selected").hide();
        var c_li = p_li.clone(true);
        //c_li.find("input").val("");
        $(this).parent().after(c_li);
        if(c_li.find("select option:visible").length < 1)
        {
            c_li.remove();
            p_li.find("select option:selected").show();
            return false;
        }
        var v = $(c_li.find("select option:visible:eq(0)")).val();
        $(c_li.find("select")).val(v);
        $(this).text("删除");
        $(this).unbind('click');
        $(this).click(function () {
           $(this.parentNode).remove();
            f();
        });
        f();
    });
    $("#modules").change(function(){
        var select_m = $("#modules option:selected").val();
        var ms = select_m.split("|");
        score = parseFloat(ms[1]);
        weighted_score = parseFloat(ms[2]);
        reload_score();
    });
    $("input[name='set_weighted']").click(function () {
        var s = score;
        console.info(s);
        if($(this).is(":checked")) {
            s = weighted_score;
        }
        var p_li = $(this.parentNode).parent();
        p_li.find("input:eq(0)").val(s);
    });
    $("li[name='li_members'] select").change(f);
    $("#btn_new").click(new_performance);
});