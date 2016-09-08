/**
 * Created by msg on 6/17/16.
 */

function set_div_show(btn_id, is_show){
    var btn = $("#" + btn_id);
    var btn_v = btn.val();
    var div_class = btn_id.replace("btn", "div");
    if (is_show == true)
    {
        $("." + div_class).show();
    }
    else{
        $("." + div_class).hide();
    }
}


$(function(){
    $("button[id^='btn_jy_']").click(function(){
        var id = this.id;
        set_div_show(id, true);
        var all_btn = $("button[id^='btn_jy_']");
        for(var i=0;i<all_btn.length;i++)
        {
            if(all_btn[i].id == id){
                continue;
            }
            else{
                set_div_show(all_btn[i].id, false)
            }
        }
    });
    $("div[class^='div_jy_']:first").show();
});