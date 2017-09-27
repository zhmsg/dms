function add_group(){
    var env = $("#ip_groups option:selected");
    var env_no = env.val();
    var env_name = env.text();
    var env_address = env.attr("title");
    var new_span = $("<span></span>");
    new_span.attr("title", env_address);
    new_span.attr("value", env_no);
    new_span.attr("about", env_name);
    new_span.append(env_name);
    new_span.append("<b>X</b>");
    new_span.click(remove_group);
    $("#div_add_group").append(new_span);
    env.remove();
}

function remove_group(){
    var env_address = this.title;
    var env_name = $(this).attr("about");
    var env_no = $(this).attr("value");
    this.remove();
    add_option("ip_groups", env_no, env_name, env_address);
}


$(function(){
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
            var t_v = $(this).attr("value");
            this.remove();
            add_option("", t_v, t_t, t_title);
        });
        $(bind_div).append(new_span);
        item.remove();
    });
    $("input[name='allow_not_login']").click(function(){
        if ($(this).is(":checked")){
            $($(this).attr("bind-el")).show();
        }
        else{
            $($(this).attr("bind-el")).hide();
        }
    });
});