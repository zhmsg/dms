/**
 * Created by msg on 3/21/17.
 */


$(document).ready(function () {
    ue = UE.getEditor('container');
    $("#btn_save").click(function () {
        var content = ue.getContent();
        var abstract = ue.getContentTxt().substr(400);
    });
});