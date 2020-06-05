/**
 * Created by msg on 6/17/16.
 */

var g_ip_vm = null;
var ss_groups = "ss_dms_ip_groups";

function receive_group_data(data){
    sessionStorage.setItem(ss_groups, JSON.stringify(data));
    g_ip_vm.exist_groups = data;
    for(var i=0;i<data.length;i++){
        for(var j= 0;j<i;j++){
            if(data[j].g_name == data[i].g_name){
                break
            }
        }
        if(j == i){
            g_ip_vm.list_name.push(data[i].g_name)
        }
    }
}

$(document).ready(function(){
    var ip_vm = new Vue({
        el: "#div_tool_ip",
        data: {
            input_ip: "",
            ip_item: {},
            exist_groups: [],
            list_name: [],
            group: "",
            group_name: ""
        },
        methods: {
            join_group: function(){
                if(this.group != ""){
                    this.group_name = this.group;
                }
                if(this.group_name == ""){
                    return false;
                }
                console.info(this.group_name);
                var g_data = {"g_name": this.group_name, "ip_value": this.ip_item.ip};
                var ip_group_url = $("#ip_group_url").val();
                my_async_request2(ip_group_url, "POST", g_data);
            },
            query_ip: function(){
                var ip_value = this.ip_item.ip;
                var ip_str = this.ip_item.ip_str;
                var local_ip = localStorage.getItem(ip_value);
                var ip_info = null;
                if(local_ip != null){
                    console.info("from local get " + local_ip);
                    ip_info = JSON.parse(local_ip);
                }
                else {
                    ip_info = get_ip_info(ip_value);
                }
                if(ip_info != null){
                    g_ip_vm.ip_item = ip_info;
                    g_ip_vm.ip_item.ip_str = ip_str;
                }
                var g_data_s = sessionStorage.getItem(ss_groups);
                var ip_groups = "";
                if(g_data_s != null){
                    var g_data = JSON.parse(g_data_s);
                    for(var i=0;i<g_data.length;i++){
                        var g_item = g_data[i];
                        if(ip_value <= g_item["ip_e"] && ip_value >= g_item["ip_s"]){
                            ip_groups += g_item["g_name"] + " ";
                            console.info(g_item);
                        }
                    }
                }
                $("#ip_group").text(ip_groups);
            }
        },
        watch:{
            input_ip: function(v, old_v){
                var ip_str = v;
                var ip_value = ip_str.search(/[^\d]+/i);
                if(ip_value != -1 || ip_str.length <= 0){
                    console.info("now input ip str");
                    ip_str = format_ip(ip_str);
                    this.ip_item.ip_str = ip_str;
                    ip_value = str_2_ip(ip_str);
                }
                else{
                    ip_value = parseInt(ip_str);
                    this.ip_item.ip_str = ip_2_str(ip_value);
                }
                if(ip_value >= 0) {

                    this.ip_item.ip = ip_value;
                }
                else{
                    this.ip_item.ip = "";
                }
                this.ip_item.info1= "";
                this.ip_item.info2= "";
                $("#ip_group").text("");
            }
        }

    });
    g_ip_vm = ip_vm;
    var request_ip = $("#request_ip").val();
    g_ip_vm.input_ip = request_ip;
    var ip_group_url = $("#ip_group_url").val();
    my_async_request2(ip_group_url, "GET", null, receive_group_data);

});