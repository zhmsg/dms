/**
 * Created by msg on 3/22/17.
 */

var q_vm = null;

function handler_query_article(data) {
    console.info(data);
    var article_count = data.length;
    for (var i = 0; i < article_count; i++) {
        var article_item = data[i];
        article_item["time_text"] = timestamp_2_datetime(article_item["update_time"]) + "   [ 作者：" + article_item["user_name"] + " ]";
        q_vm.articles.push(article_item);
    }

}

$(document).ready(function () {

    var r_url = location.href;
    my_async_request2(r_url, "GET", null, handler_query_article);
    $("#btn_add_article").click(function () {
        window.open($("#url_add_article").val());
    });
    $("#btn_query").click(function(){
        console.info("query");
        var q_value = $("#query_str").val().trim(" ");
        var div_l = $(".articleList");
        var li_articles = div_l.find("li");
        var li_len = li_articles.length;
        for(var i=0;i<li_len;i++){
            var li_item = $(li_articles[i]);
            li_item.hide();
            if(q_value.length == 0){
                li_item.show();
            }
            else{
                if(li_item.text().indexOf(q_value) >= 0){
                    li_item.show();
                }
            }

        }
    });
    $(function(){
        document.onkeydown = function(e){
            var ev = document.all ? window.event : e;
            if(ev.keyCode==13) {
                $("#btn_query").click();
             }
        }
    });
    var current_user_name = "";
    if ($("#current_user_name").length > 0) {
        current_user_name = $("#current_user_name").val();
    }
    var url_prefix= $("#url_add_article").val();
    q_vm = new Vue({
        el: "#article_list",
        data: {
            current_user_name: current_user_name,
            url_prefix: url_prefix,
            articles: []
        },
        methods: {

        }
    })
});