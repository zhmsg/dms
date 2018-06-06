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
            messages: []
        }
    });
    my_async_request2($("#url_cache_messages").val(), "GET", null, function(data){
        for(var i=0; i<data.length;i++){
            var item = data[i];
            item.publish_time = timestamp_2_datetime(item.publish_time, true);
            vm.messages.push(item);
        }
    });
});