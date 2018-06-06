/**
 * Created by msg on 6/6/18.
 */

$(document).ready(function () {
    var vm = new Vue({
        el: "#div_messages",
        data: {
            test: "VUE",
            messages: [
                {"message_tag": "TEST", "publish_time": "2018"}
            ]
        }
    })
    //var app4 = new Vue({
    //    el: '#app-4',
    //    data: {
    //        todos: [
    //            {text: '学习 JavaScript'},
    //            {text: '学习 Vue'},
    //            {text: '整个牛项目'}
    //        ]
    //    }
    //})
});