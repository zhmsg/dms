/**
 * Created by msg on 10/29/15.
 */
// $('#search_table').bind('input propertychange', function() {alert("success")});

function search_table(){
    var v = $("#search_table").val();
    var a_el = $("a");
    var len_a = a_el.length;
    for(var i=0;i<len_a;i++){
        a_el[i].hidden = true;
        if(v.length == 0){
            a_el[i].hidden = false;
        }
        else if(a_el[i].text.indexOf(v) >= 0){
            a_el[i].hidden = false;
        }
        else{
            a_el[i].hidden = true;
        }
    }
}