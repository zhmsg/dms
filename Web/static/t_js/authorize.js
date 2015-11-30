/**
 * Created by msg on 11/23/15.
 */


function user_select_change(){
    var role_value = JSON.parse($("#role_value").text());
    var selected_user = $("#perm_user option:selected");
    var user_role = parseInt(selected_user.attr("role"));
    console.info(user_role);
    for(var role in role_value) {
        console.info(role);
        var role_el = document.getElementById(role);
        if(role_el == null){
            continue;
        }
        if((role_value[role] & user_role) == role_value[role]){
            role_el.checked = true;
        }
        else{
            role_el.checked = false;
        }
    }

}
