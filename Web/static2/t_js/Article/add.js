/**
 * Created by msg on 3/21/17.
 */

function handler(data) {
    if ("article_no" in data) {
        $("#article_no").val(data.article_no);
    }
    if ("content" in data && "title" in data) {
        $("#article_title").val(data.title);
        ue.setContent(data.content);
    }
    else {
        alert1("保存成功");
    }
}

function save_article() {
    var title = $("#article_title").val();
    var content = ue.getContent();
    var abstract = ue.getContentTxt().substr(0, 400);
    var article_no = $("#article_no").val();
    var method = "POST";
    var r_data = {"content": content, "abstract": abstract, "title": title};
    if (article_no.length == 32) {
        r_data["article_no"] = article_no;
        method = "PUT";
        var r_url = location.href;
        my_async_request2(r_url, method, r_data, handler);
    }
}

$(document).ready(function () {
    ue = UE.getEditor('container');
    ue.ready(function () {
        var article_no = $("#article_no").val();
        if (article_no.length == 32) {
            var r_url = location.href;
            my_async_request2(r_url, "GET", null, handler);
        }
    });
    window.setInterval(save_article, 60000);
    $("#btn_save").click(function () {
        var title = $("#article_title").val();
        if (title.length < 3) {
            alert1("标题不可少于3个字符");
            return;
        }
        var content = ue.getContent();
        var abstract = ue.getContentTxt().substr(0, 400);
        var article_no = $("#article_no").val();
        var method = "POST";
        var r_data = {"content": content, "abstract": abstract, "title": title};
        if (article_no.length == 32) {
            r_data["article_no"] = article_no;
            method = "PUT";
        }
        var r_url = location.href;
        my_async_request2(r_url, method, r_data, handler);
    });
});