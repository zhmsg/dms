/**
 * Created by msg on 11/23/15.
 */


function user_select_change(){
    var role_value = JSON.parse($("#role_desc").text());
    var selected_user = $("#perm_user option:selected");
    var user_role = parseInt(selected_user.attr("role"));

    for(var role_module in role_value) {
        var role_list = role_value[role_module]["role_list"];
        for(var role in role_list) {
            var role_el = document.getElementById(role);
            if (role_el == null) {
                continue;
            }
            if ((role_list[role]["role_value"] & user_role) == role_list[role]["role_value"]) {
                role_el.checked = true;
            }
            else {
                role_el.checked = false;
            }
        }
    }

}
user_select_change();