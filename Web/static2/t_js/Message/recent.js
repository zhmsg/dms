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
            login_url: "/?next=" + location.href,
            need_login: need_login,
            messages: []
        }
        //methods: {
        //    look_msg: function(index){
        //        var show = this.messages[index].show;
        //        this.messages[index].show = !show;
        //    }
        //}
    });
    if(need_login == false) {
        my_async_request2($("#url_cache_messages").val(), "GET", null, function (data) {
            for (var i = 0; i < data.length; i++) {
                var item = data[i];
                item.show = false;
                if("readable_content" in item){
                    item.readable_content = item.readable_content.replace("\n", "<br/>")
                }
                item.publish_time = timestamp_2_datetime(item.publish_time, true);
                vm.messages.push(item);
            }
        });
    }
});