/**
 * Created by msg on 12/6/16.
 */

function load_log_info(data){
    $("#btn_query_log").removeAttr("disabled");
    if(data.length < 1){
        $("#log_no").val("日志编号不存在，请核对后重试");
        return false;
    }
    var log_info = data[0];
    $("#log_no").val(log_info.log_no);
    $("#run_begin").val(log_info.run_begin);
    $("#account").val(log_info.account);
    $("#level").val(log_info.level);
    $("#run_time").val(log_info.run_time);
    $("#ip").val(log_info.ip);
}

$(document).ready(function(){
    $("#query_log_no").keyup(function(){
        var v = $("#query_log_no").val();
        v = v.replace(/([^\d]*)/g, "");
        $("#query_log_no").val(v);
    });
	$("#btn_query_log").click(function () {
        var query_log_no = $("#query_log_no").val();
        if(query_log_no.length < 14){
            $("#log_no").val("无效的日志编号，请核对后重试");
            return false;
        }
        $("#btn_query_log").attr("disabled", "disabled");
        var request_url = $("#url_prefix").val() + "/";
        my_async_request2(request_url, "POST", {"log_no": query_log_no}, load_log_info)
    });
});
