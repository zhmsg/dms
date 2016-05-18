/**
 * Created by msg on 12/24/15.
 */

var module_info = new Object();
var error_type = new Object();

function get_module_info() {
    var request_url = $("#fun_info_url").val();
    console.info(request_url);
    $.ajax({
        url: request_url,
        method: "GET",
        success: function (data) {
            if (data.status == true){
                module_info = data.data;
                var module_row = new Array();
                var i = 0;
                for(var key in module_info){
                    var data = new Array();
                    data[0] = key;
                    data[1] = module_info[key].title;
                    data[2] = module_info[key].desc;
                    data[3] = "<a href='#'>删除</a>";
                    module_row[i] = data;
                    i++;
                }
                console.info(module_row);
                add_table_row("tb_main_module", module_row);
                set_service_id();
            }
        },
        error: function (xhr) {
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            console.info(res);
        }
    });
}
function get_error_type() {
    var request_url = $("#error_type_url").val();
    console.info(request_url);
    $.ajax({
        url: request_url,
        method: "GET",
        success: function (data) {
            if (data.status == true){
                error_type = data.data;
                set_error_type();
            }
        },
        error: function (xhr) {
            var res = "状态码：" + xhr.status + "\n";
            res += "返回值：" + xhr.statusText + "";
            console.info(res);
        }
    });
}

function add_option(select_obj, value, text){
    var option = "<option value='{value}'>{text}</option>";
    var option_item = option.replace("{value}", value).replace("{text}", text);
    select_obj.append(option_item);
}

function set_service_id(){
    var select_obj = $("#service_id");
    select_obj.empty();
    for(var key in module_info){
        add_option(select_obj, key, module_info[key].title);
    }
    set_fun_id();
}
function set_fun_id(){
    var service_id = $("#service_id").val();
    var fun_list = module_info[service_id]["fun_info"];
    var mul_row = new Array();
    var i = 0;
    for(var key in fun_list){
        var row_data = new Array();
        row_data[0] = key;
        row_data[1] = fun_list[key].title;
        row_data[2] = fun_list[key].desc;
        row_data[3] = "<a href='#'>删除</a>";
        mul_row[i] = row_data;
        i++;
    }
    add_table_row("tb_sub_module", mul_row, true);
}

function set_error_type(){
    var select_obj = $("#type_id");
    var mul_select_obj = $("#mul_type_id");
    select_obj.empty();
    mul_select_obj.empty();
    for(var key in error_type){
        add_option(select_obj, key, error_type[key].title);
        if(error_type[key].title.substr(0, 2) == "参数") {
            add_option(mul_select_obj, key, error_type[key].title);
        }
    }

}




function get_info(code){
    var service_id = code.substr(0, 2);
    var service_title = module_info[service_id].title;
    var fun_id = code.substr(2, 2);
    var fun_title = module_info[service_id]["fun_info"][fun_id].title;
    var type_id = code.substr(4, 2);
    var type_title = error_type[type_id].title;
    var info = service_title + "<br />" + fun_title + "<br />" + type_title;
    return info;
}

//$(function(){
//    //鼠标移入显示 移出消失 的效果
//    $("tr[id^='s_']").hover(
//        function(){
//            var code_info = get_info(this.id.substr(2,8));
//            $("#status_code_info").html(code_info);
//            $(".status_out").show();
//            $(".status_out").css('top',(this.offsetHeight + this.offsetTop)+'px')
//        },
//        function(){
//            $(".status_out").hide()
//        }
//    );
//});
function set_div_show(btn_id, is_show){
    var btn = $("#" + btn_id);
    var btn_v = btn.val();
    var div_class = btn_id.replace("btn", "div");
    if (is_show == true)
    {
        btn.html("隐藏" + btn_v);
        $("." + div_class).show();
    }
    else{
        btn.html(btn_v);
        $("." + div_class).hide();
    }
}
function div_show(btn_id)
{
    var btn = $("#" + btn_id);
    var btn_v = btn.val();
    var btn_html = btn.html();
    if(btn_v == btn_html){
        set_div_show(btn_id, true);
        return true;
    }
    else
    {
        set_div_show(btn_id, false);
        return false;
    }
}

$(function(){
    $("button[id^='btn_new_']").click(function(){
        var id = this.id;
        div_show(id);
        var all_btn = $("button[id^='btn_new_']");
        for(var i=0;i<all_btn.length;i++)
        {
            if(all_btn[i].id == id){
                continue;
            }
            else{
                set_div_show(all_btn[i].id, false)
            }
        }
    });
});


function add_table_row(table_id, mul_row, clear){
    var t = $("#" + table_id);

    if(clear == true){
        t.empty();
    }
    var row_len = mul_row.length;
    for(var i=0;i<row_len;i++){
        var row = $("<tr></tr>");
        var row_data = mul_row[i];
        var data_len = row_data.length;
        for(var j=0;j<data_len;j++){
            var td = $("<td></td>");
            td.append(row_data[j]);
            row.append(td);
        }
        t.append(row);
    }

}
$(function(){
    get_module_info();
    //get_error_type();
});