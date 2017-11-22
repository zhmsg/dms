
function add_key()
{
    var app = $("#app").val();
    var effective_days = $("#effective_days").val();
    var deadline = new Date().getTime() / 1000 + 3600 * 24 * effective_days;
    var remark = $("#remark").val();
    var data = {"app": app, "deadline": deadline, "ip_auth": false, "remark": remark};
    if ($("input[name='ip_auth']:visible").is(":checked")){
        data["ip_auth"] = true;
        var group_spans = $("#div_add_group").find("span");
        var gs_len = group_spans.length;
        var ip_groups = new Array();
        for(var i=0;i<gs_len;i++){
            var v = $(group_spans[i]).attr("value");
            ip_groups[i] = v;
        }
        data["ip_groups"] = ip_groups;
    }
    var key_info = $("li[name='key_info']:visible");
    var ki_len = key_info.length;
    for(var j=0;j<ki_len;j++)
    {
        var li_item = $(key_info[j]);
        var li_input = li_item.find("input");
        var k = $(li_input[0]).val();
        var v = $(li_input[1]).val();
        if($(li_input[2]).is(":checked")){
            k = "_" + k;
        }
        data[k]= v;
    }
    console.info(data);
    my_async_request2(location.href, "POST", data);
}

function load_groups(data){
    var data_len = data.length;
    for(var i=0;i<data_len;i++){
        var d_item = data[i];
        add_option("ip_groups", d_item["g_name"], d_item["g_name"], d_item["remark"]);
    }
}

$(document).ready(function () {
    my_async_request2($("#ip_group_url").val(), "GET", null, load_groups);
    $("span[name='span_add']").click(function(){
        var bind_select = $(this).attr("bind-select");
        var bind_div = $(this).attr("bind-div");
        var item = $(bind_select + " option:selected");
        var v = item.val();
        var t = item.text();
        var title = item.attr("title");
        var new_span = $("<span></span>");
        new_span.attr("title", title);
        new_span.attr("value", v);
        new_span.attr("about", t);
        new_span.append(t);
        new_span.append("<b>X</b>");
        new_span.click(function(){
            var t_title = this.title;
            var t_t = $(this).text();
            t_t = t_t.substr(0, t_t.length - 1);
            var t_v = $(this).attr("value");
            this.remove();
            add_option(bind_select, t_v, t_t, t_title);
        });
        $(bind_div).append(new_span);
        item.remove();
    });
    $("input[name='ip_auth']").click(function(){
        if ($(this).is(":checked")){
            $($(this).attr("bind-el")).show();
        }
        else{
            $($(this).attr("bind-el")).hide();
        }
    });
    $("a[name='link_add_input']").click(function(){
        var p_li = $(this.parentNode);
        var c_li = p_li.clone(true);
        c_li.find("input").val("");
        $(this).parent().after(c_li);
        $(this).text("删除");
        $(this).unbind('click');
        $(this).click(function () {
           $(this.parentNode).remove();
        });
    });
    $("#btn_new_key").click(add_key);
});