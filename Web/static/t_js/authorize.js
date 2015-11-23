/**
 * Created by msg on 11/23/15.
 */


function user_select_change(){
    var role_value = JSON.parse($("#role_value").text());
    var selected_user = $("#perm_user option:selected");
    var user_role = parseInt(selected_user.attr("role"));
    console.info(user_role);
    for(var role in role_value) {
        if((role_value[role] & user_role) == role_value[role]){
            document.getElementById(role).checked = true;
        }
        else{
            document.getElementById(role).checked = false;
        }
    }

}
