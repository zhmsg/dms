/**
 * Created by msg on 3/21/17.
 */

function handler(data) {
    if ("article_no" in data) {
        $("#article_no").val(data.article_no);
    }
    if ("content" in data && "title" in data) {
        $("#article_title").text(data.title);
        document.title = data.title;
        $("#container").html(data.content);
    }
}

$(document).ready(function () {
    var article_no = $("#article_no").val();
    if (article_no.length == 32) {
        var r_url = location.href;
        my_async_request2(r_url, "GET", null, handler);
    }
});