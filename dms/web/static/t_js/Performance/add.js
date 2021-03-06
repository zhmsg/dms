
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
    all_users = data;
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
            option_item.removeAttr("disabled");
            var option_value = option_item.val();
            for(var k=0; k<lis_len; k++){
                if(option_value == members[k] && k != i){
                    option_item.attr("disabled", "disabled");
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
    if(name.length <= 0){
        popup_show("必须输入名称");
        return false;
    }
    var detail_info = $("#detail_info").val();
    if(detail_info.length <= 0){
        popup_show("必须输入详情地址");
        return false;
    }
    var start_time = datetime_2_timestamp($("#start_time").val());
    if(isNaN(start_time)){
        popup_show("请输入正确的开始时间");
        return false;
    }
    var end_time = datetime_2_timestamp($("#end_time").val());
    if(isNaN(end_time)){
        popup_show("请输入正确的结束时间");
        return false;
    }
    if(end_time < start_time){
        popup_show("结束时间不能小于开始时间");
        return false;
    }
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
    my_async_request2(location.href, "POST", data);
}

$(document).ready(function () {
    my_async_request2($("#module_url").val(), "GET", null, load_modules);
    my_async_request2($("#list_user_url").val(), "GET", null, load_users);
    $("a[name='link_add_input']").click(function(){
        var p_li = $(this).parent();
        p_li.find("select option:selected").hide();
        p_li.find("select option:selected").attr("disabled", "disabled");
        var c_li = p_li.clone(true);
        p_li.find("select option:selected").show();
        p_li.find("select option:selected").removeAttr("disabled");
        p_li.after(c_li);
        if(c_li.find("select option:enabled").length < 1)
        {
            c_li.remove();
            return false;
        }
        var v = $(c_li.find("select option:enabled:eq(0)")).val();
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