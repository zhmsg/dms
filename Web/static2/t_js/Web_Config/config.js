/**
 * Created by zhouhenglc on 2019/11/20.
 */

var config_vm = null;

$(function(){
    var o_keys = UrlArgsValue(location.href, "keys");
    if(o_keys == null){
        var keys = [];
    }
    else{
        var keys = o_keys.split(",");
    }
    var config_keys = {};
    for(var index in keys){
        config_keys[keys[index]] = {'value': ''}
    }
    var values_url = "/config/values";
    my_request2(values_url, "GET", {'keys': o_keys}, function (data) {
        for(var key in data){
            var value = data[key];
            if(value != null){
                config_keys[key]['origin_value'] = value.config_value;
                config_keys[key]['value'] = value.config_value;
            }
        }
    });
    config_vm = new Vue({
        el: "#div_config",
        data: {
            config_keys: config_keys
        },
        methods: {
            submit_action: function(){
                var data = {};
                var has_update = false;
                for(var key in this.config_keys){
                    if(this.config_keys[key].value != this.config_keys[key].origin_value) {
                        data[key] = this.config_keys[key].value;
                        has_update = true;
                    }
                }
                console.info(data);
                if(has_update == false){
                    alert1("无更新无需提交");
                    return false;
                }
                my_async_request2(values_url, 'POST', data, function(data){
                    alert1("更新成功！");
                    location.reload();
                })
            }
        }
    });

});