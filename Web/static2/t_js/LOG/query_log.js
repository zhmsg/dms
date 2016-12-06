/**
 * Created by msg on 12/6/16.
 */

function load_log_info(data){
    $("input:text[readonly]").val("");
    $("textarea").val("");
    $("#btn_query_log").removeAttr("disabled");
    if(data.length < 1){
        $("#log_no").val("日志编号不存在，请核对后重试");
        return false;
    }
    var log_info = data[0];

    $("#log_no").val(log_info.log_no);
    $("#run_begin").val(new Date(log_info.run_begin * 1000).toLocaleString());
    $("#request_url").val(log_info.host + log_info.url.substr(1));
    $("#account").val(log_info.account);
    $("#level").val(log_info.level);
    $("#run_time").val(log_info.run_time);
    $("#ip").val(ip_2_str(log_info.ip));
    if(log_info.level == "info"){
        $("#request_info").val("调用正常，不记录请求信息。");
        $("#error_info").val("调用正常，无错误信息。");
    }
    else{
        var index = log_info.info.indexOf("\n");
        if(index >= 0) {
            $("#request_info").val(format_json_str(log_info.info.substr(0, index)));
            var left_info = log_info.info.substring(index + 1, log_info.info.length);
            $("#error_info").val(format_json_str(left_info));

        }
        else{
            $("#error_info").val(log_info.info);
        }
    }
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
    var log_no = UrlArgsValue(location.href, "log_no");
    if(log_no != null){
        $("#query_log_no").val(log_no);
        $("#btn_query_log").click();
    }
});
