/**
 * Created by msg on 10/27/16.
 */

function bit_and(role1, role2){
    var v = role1 & role2;
    if(v < role1 && v < role2)
        return false;
    else
        return true;
}

function escape(s) {
 return s.replace(/[<>&"]/g,function(c){return {'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c];});
}