/**
 * Created by msg on 6/6/18.
 */

$(document).ready(function () {
    var need_login = false;
    if ($("#current_user_name").length <= 0) {
        var need_login = true;
    }
    var vm = new Vue({
        el: "#div_messages",
        data: {
            need_login: need_login,
            test: "VUE",
            messages: [
                {"message_tag": "TEST", "publish_time": "2018"}
            ]
        }
    });
    my_async_request2($("#url_cache_messages").val(), "GET", null, function(data){
       vm.messages =  data;
    });
});