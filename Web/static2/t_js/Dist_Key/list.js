
function load_keys(data){
    console.info(data);
}


$(document).ready(function () {
    var query_url = $("#query_url").val();
    my_async_request2(query_url, "POST", {}, load_keys)
});