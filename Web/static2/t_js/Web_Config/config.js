/**
 * Created by zhouhenglc on 2019/11/20.
 */

var config_vm = null;

$(function(){
    config_vm = new Vue({
        el: "#div_config",
        data: {
            config: null
        },
        methods: {
            change_tab: function(key){
                for(var _key in this.tabs_class){
                    this.tabs_class[_key]['active'] = "";
                }
                if(key == ""){
                    this.has_params = false;
                    return false;
                }
                this.params = this.tabs_class[key]['params'];
                this.has_params = true;
                this.tabs_class[key]['active'] = "active";
            },
            update_url_action: function () {
                update_request_url();
            },
            test_api_action: function(){
                test_api22();
                storage_action();
            },
            add_sub_params: function(parent_item){
                var ns_item = {};
                var keys = ["param_name", "param_type", "necessary", "param_desc"];
                for(var k_i in keys){
                    var key = keys[k_i];
                    ns_item[key] = parent_item.sub_param_item[key];
                }
                parent_item.sub_params.push(ns_item);
                return ns_item
            },
            delete_sub_params: function(parent_item, index){
                parent_item.sub_params.splice(index, 1);
            }
        },
        watch: {
            use_env: function(val){
                update_request_url(val);
                return val;
            }
        }
    });

});