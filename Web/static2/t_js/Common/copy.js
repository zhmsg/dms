/**
 * Created by msg on 3/2/17.
 */

function copy_text(s)
{
    var aux = document.createElement("input");
    aux.setAttribute("value", s);
    document.body.appendChild(aux);
    aux.select();
    document.execCommand("copy");
    document.body.removeChild(aux);

    $(".popup_div_1").hide();
    s = escape(s);
    var pop_div = $('<div class="popup_div_1 display_none" name="pop_div"><div class="popup_content_1">成功复制' + s +'</div></div>');
    $("body").append(pop_div);
    pop_div.show();
    reset_bottom();

    window.setTimeout(function(){
        pop_div.remove();
    }, 3000);

    window.onresize = function() {
        reset_bottom();
    };
}

function reset_bottom()
{
    $(".popup_div_1").each(function(){
        var div_el = $(this);
        var height = $(window).height();
        var width = $(window).width();
        div_el.css({'left': (width / 2 - div_el.width() / 2) + "px", 'top': (height - div_el.height() - 40) + 'px'});
    });
}
