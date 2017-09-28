
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
            t_t = t_t.substr(0, t_t.length - 1);
            var t_v = $(this).attr("value");
            this.remove();
            add_option(bind_select, t_v, t_t, t_title);
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
});