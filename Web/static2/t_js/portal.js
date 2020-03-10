/**
 * Created by msg on 10/20/16.
 */

function bit_and(role1, role2){
    var v = role1 & role2;
    if(v < role1 && v < role2)
        return false;
    else
        return true;
}

$(function(){
    var current_user_role = parseInt($("#current_user_role").val());
    if(current_user_role > 0) {
        var current_href = location.href.substr((location.protocol + "//" + location.host).length);
        if(current_href.indexOf("/tornado") == 0){
            $("#div_current_env").append('<a href="' + current_href.substr(8) + '">' + '还用Flask' + '</a>');
        }
        else{
            $("#div_current_env").append('<a href="/tornado' + current_href + '">' + '体验Tornado' + '</a>');
        }
    }
});