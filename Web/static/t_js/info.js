/**
 * Created by msg on 9/17/15.
 */

function get_info(type,data_no){
    $.ajax({
        url: "/dms/" + type + "/?data_no=" + data_no,
        type: "GET",
        async: false,
        success: function (data) {
            //alert(data);
            data_object = JSON.parse(data);
            if(data_object.status == false){
                $("#info").html(data_object.data);
            }
            else{
                var value = data_object.value;
                var ch = data_object.ch;
                var att = data_object.att;
                var info_str = "数据编号:" + data_no + "<br>";
                for(var i=0;i<att.length;i++){
                    info_str += ch[i] + ":" + value[att[i]] + "<br>"
                }
                $("#info").html(info_str)
            }
        },
        error: function () {
            $("#info").html("获取失败，请点击重试");
        }
    });
}
