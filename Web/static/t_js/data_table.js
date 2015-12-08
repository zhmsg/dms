/**
 * Created by msg on 10/29/15.
 */
// $('#search_table').bind('input propertychange', function() {alert("success")});

function msg_include(str, include_str){
    var len_include = include_str.length;
    var len_str = str.length;
    var i= 0, j=0;
    while(true){
        if(i >= len_include){
            return true;
        }
        if(j >= len_str){
            return false;
        }
        if(str[j] == include_str[i]){
            i++;
            j++;
        }
        else{
            j++;
        }
    }
}

function search_table(){
    var v = $("#search_table").val();
    var a_el = $("a");
    var len_a = a_el.length;
    for(var i=0;i<len_a;i++){
        var a_href = a_el[i].attributes["title"].value + "&query=" + v;
        a_el[i].href = a_href;
        a_el[i].hidden = true;
        if(v.length == 0){
            a_el[i].hidden = false;
        }
        else if(msg_include(a_el[i].text, v)){
            a_el[i].hidden = false;
        }
        else{
            a_el[i].hidden = true;
        }
    }
}
search_table();
