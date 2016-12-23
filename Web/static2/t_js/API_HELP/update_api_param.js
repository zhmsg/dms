/**
 * Created by msg on 3/18/16.
 */

function Load_API_Module(data){
    var part_len = data.length;
    for(var i=0;i<part_len;i++){
        var module_list = data[i].module_list;
        var module_len = module_list.length;
        for(var j=0;j<module_len;j++){
            var module_item = module_list[j];
            add_option("target_api_module", module_item["module_no"], module_item["module_name"], module_item["module_desc"]);
            add_option("source_api_module", module_item["module_no"], module_item["module_name"], module_item["module_desc"]);
        }
    }
}


$(function(){
    var request_url = $("#module_url").val();
    my_request2(request_url, "GET", null, Load_API_Module);
});