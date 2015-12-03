/**
 * Created by msg on 12/3/15.
 */

function test_api(){
    var param_el = $("input[id$='_value']");
    console.info(param_el);
    for(var i=0;i<param_el.length;i++){
        var el = param_el[i];
        console.info(el.id);
        console.info(el.attributes["param_type"].value);
        console.info(el.value);
    }
    $.ajax({
        url: "http://127.0.0.1:58000/api/v3/oauth2/token/ping/?callback=?",
        dataType:'json',
        method: "GET",
        success:function(data){
            alert(data.message);
        },
        error:function(xhr){
            console.info(xhr);
            alert(xhr.statusText + xhr.status);
        }
    });
}

