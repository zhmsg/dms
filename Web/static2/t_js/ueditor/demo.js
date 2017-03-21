/**
 * Created by msg on 3/21/17.
 */


$(document).ready(function () {
    ue = UE.getEditor('container');
    $("#btn_save_all_html").click(function () {
        DownloadFile("demo_all_html.doc", ue.getAllHtml());
    });
    $("#btn_save_content").click(function () {
        DownloadFile("demo_content_html.doc", ue.getContent());
    });
    $("#btn_save_content_text").click(function () {
        DownloadFile("demo_content_text.doc", ue.getContentTxt());
    });
    $("#btn_save_plain_text").click(function () {
        DownloadFile("demo_plain_text.doc", ue.getPlainTxt());
    });
});