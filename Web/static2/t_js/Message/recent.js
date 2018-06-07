/**
 * Created by msg on 6/6/18.
 */

function load_message(vm)
{
    var data = {start: vm.start, end: vm.end};
    my_async_request2($("#url_cache_messages").val(), "GET", data, function (data) {
        for (var i = 0; i < data.length; i++) {
            var item = data[i];
            item.show = false;
            item.message_content = item.message_content.replace(/\n/g, "<br/>");
            if ("readable_content" in item) {
                item.readable_content = item.readable_content.replace(/\n/g, "<br/>")
            }
            item.publish_time = timestamp_2_datetime(item.publish_time, true);
            vm.messages.push(item);
        }
        if (data.length + vm.start == vm.end) {
            vm.can_load = true;
            vm.start = vm.end;
            vm.end = vm.start + 10;
        }
        else {
            vm.can_load = false;
        }
    });
}

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
            messages: [],
            can_load: false,
            start: 0,
            end: 10
        },
        methods: {
            look_msg: function(index){
                var show = this.messages[index].show;
                this.messages[index].show = !show;
            },
            load_more: function(){
                console.info("start load more");
                load_message(this);
            }
        }
    });
    if(need_login == false) {
        load_message(vm);
    }
});