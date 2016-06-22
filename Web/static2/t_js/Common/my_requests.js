/**
 * Created by msg on 5/21/16.
 */

function request_error(xhr){
    var res = "状态码：" + xhr.status + "\n";
    res += "返回值：" + xhr.statusText + "";
    console.info(xhr);
    sweetAlert(xhr.responseText);
}

function my_request(request_url, request_method, body_param, request_success){
    if(request_method != "GET"){
        body_param = JSON.stringify(body_param)
    }
    $.ajax({
        url: request_url,
        method: request_method,
        contentType: "application/json",
        data: body_param,
        async:false,
        success:request_success,
        error:request_error
    });
}

function my_async_request(request_url, request_method, body_param, request_success){
    if(request_method != "GET"){
        body_param = JSON.stringify(body_param)
    }
    $.ajax({
        url: request_url,
        method: request_method,
        contentType: "application/json",
        data: body_param,
        success:request_success,
        error:request_error
    });
}