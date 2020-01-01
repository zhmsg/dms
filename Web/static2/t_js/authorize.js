/**
 * Created by msg on 11/23/15.
 */

var auth_vm = null;

function bit_and(a, b) {
    var c = 1;
    var r = 0;
    while (a > 0 && b > 0) {
        if (a % 2 == 1 && b % 2 == 1) {
            r += c;
        }
        a = (a - a % 2) / 2;
        b = (b - b % 2) / 2;
        c = c * 2;
    }
    return r;
}

function user_select_change(){
    var role_value = JSON.parse($("#role_desc").text());
    var selected_user = $("#perm_user option:selected");
    var user_role = parseInt(selected_user.attr("role"));
    if(user_role == 0){
        $("#link_remove_user").show();
    }
    else{
        $("#link_remove_user").hide();
    }
    for(var role_module in role_value) {
        var role_list = role_value[role_module]["role_list"];
        for(var role in role_list) {
            var role_el = document.getElementById(role);
            if (role_el == null) {
                continue;
            }
            if (bit_and(role_list[role]["role_value"], user_role) == role_list[role]["role_value"]) {
                role_el.checked = true;
            }
            else {
                role_el.checked = false;
            }
        }
    }

}

function reload(data){
    location.reload();
}

function remove_user(){
    var selected_user = $("#perm_user option:selected").val();
    var r_url = $("#link_remove_user").attr("url");
    my_async_request2(r_url, "DELETE", {"user_name": selected_user}, reload);
}
$(function() {
    var url = '/user/policies/manager';
    var man_policies = {};
    my_request2(url, 'GET', null, function(data){
       man_policies = data;
    });
    for(var key in man_policies){
        var p_item = man_policies[key];
        p_item['policies_l'] = [{'desc': '准入', 'key': 'basic', 'checked': ''}];
        for(var s_key in p_item['policies']){
            var _item = p_item['policies'][s_key];
            _item['key'] = s_key;
            _item['checked'] = '';
            p_item['policies_l'].push(_item);
        }
        p_item['policies_l'].push({'desc': '管理员', 'key': 'manager', 'checked': ''});
    }

    auth_vm = new Vue({
        el: "#div_auth",
        data: {
            other_user: "",
            man_policies: man_policies
        },
        methods: {
            check_policies: function(){
                var o_user = this.other_user;
                console.info(o_user);
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