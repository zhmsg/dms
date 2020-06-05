/**
 * Created by msg on 3/22/17.
 */

var q_vm = null;

function handler_query_article(data) {
    console.info(data);
    q_vm.articles = [];
    var article_count = data.length;
    for (var i = 0; i < article_count; i++) {
        var article_item = data[i];
        var brow_times = article_item["self_read_times"] + article_item["read_times"];
        article_item["time_text"] = timestamp_2_datetime(article_item["update_time"]) + " [ 作者：" + article_item["user_name"] + " ][浏览" + brow_times + "]";
        q_vm.articles.push(article_item);
    }

}

$(document).ready(function () {

    var r_url = location.href;
    my_async_request2(r_url, "GET", null, handler_query_article);

    var current_user_name = "";
    if ($("#current_user_name").length > 0) {
        current_user_name = $("#current_user_name").val();
    }
    var url_prefix= $("#url_add_article").val();
    q_vm = new Vue({
        el: "#article_container",
        data: {
            current_user_name: current_user_name,
            url_prefix: url_prefix,
            query_str: "",
            articles: []
        },
        methods: {
            query_action: function(){
                my_async_request2(r_url, "GET", {"query_str": this.query_str}, handler_query_article);
            },
            to_new: function(){
                window.open(this.url_prefix);
            }
        }
    })
});