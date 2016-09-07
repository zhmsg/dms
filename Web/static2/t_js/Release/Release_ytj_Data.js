/**
 * Created by msg on 9/7/16.
 */

function receive_success(data)
{
    console.info(data);
}

function receive_secret_key(){
    var request_url = "http://local.gene.ac:3285/yitiji/fabu/";
    my_async_request(request_url, "POST", null, receive_success);
}


$(function(){
    //receive_secret_key();
});