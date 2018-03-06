var all_users = null;

function load_performance(data) {
    var current_user = $("#current_user_name").val();

    var pr_items = data["detail"];
    var statistics = data["statistics"];

    draw_stacked_bar_chart("#svg_total", statistics.columns, statistics.data);
    for(var i=1; i<statistics.columns.length; i++){
        var add_field = $('<fieldset></fieldset>');
        var add_legend = $('<legend></legend>');
        add_legend.text(statistics.columns[i]);
        add_field.append(add_legend);
        var add_svg = $('<svg width="860" height="500"></svg>');
        var svg_id = "svg_" + i;
        add_svg.attr("id", svg_id);
        add_field.append(add_svg);
        $("#div_svg").append(add_field);
        draw_bar_chart("#" + svg_id, statistics.data, "nick_name", statistics.columns[i]);
    }
    var pr_len = pr_items.length;

    var keys = ["month", "module_no", "name", "start_time", "end_time", "user_name", "score", "detail_info"];
    for(var i=0; i<pr_len; i++){
        var pr_item = pr_items[i];
        var main_tr_id = "tr_" + pr_item["id"];
        if(pr_item.members.length > 0){
            var prm_item = $.extend({}, pr_item, pr_item.members[0]);
            prm_item["score"] = prm_item["score"] / 1000;
            prm_item["start_time"] = timestamp_2_date(pr_item["start_time"]);
            prm_item["end_time"] = timestamp_2_date(pr_item["end_time"]);
            var reg = /https?:\/\/(\w|=|\?|\.|\/|\&|-)+/ig;
            if(reg.test(prm_item["detail_info"])){
                prm_item["detail_info"] = "<a href='" + prm_item["detail_info"] + "' target='_blank'> " + "查看" + " </a>";
            }
            var main_tr = $("<tr></tr>");
            for(var k=0; k<keys.length; k++){
                var td = new_td(keys[k], prm_item);
                main_tr.append(td);
            }
            if(pr_item.members.length > 1) {
                var span_user = $("<span></span>");
                span_user.text(prm_item["user_name"]);
                var link_more = $('<a class="status_move" name="link_more">[+]</a>');
                var user_td = main_tr.find("td[name='td_user_name']");
                user_td.text("");
                user_td.append(span_user);
                user_td.append(link_more);
                main_tr.click(function(){
                   var tr_id = $(this).attr("id");
                   var link = $(this).find("a[name='link_more']");
                   if(link.text() == "[+]"){
                       link.text("[-]");
                       $('tr[id^="' + tr_id + '_"]').show();
                   }
                    else{
                       link.text("[+]");
                       $('tr[id^="' + tr_id + '_"]').hide();
                   }
                });
            }
            $("#t_mine").append(main_tr);
            main_tr.attr("id", main_tr_id);
        }
        for(var j=1;j<pr_item.members.length; j++){
            var m_item = pr_item.members[j];
            m_item["score"] = m_item["score"] / 1000;
            if(m_item["user_name"] == current_user){
                $("#" + main_tr_id + " td[name='td_user_name'] span").text(m_item["user_name"]);
                $("#" + main_tr_id + " td[name='td_score']").text(m_item["score"]);
                m_item = pr_item.members[0];
                m_item["score"] = m_item["score"] / 1000;
            }
            var add_tr = $("<tr></tr>");
            var add_td = $("<td></td>");
            add_td.attr("colSpan", 5);
            add_tr.append(add_td);

            add_tr.append(new_td("user_name", m_item));
            add_tr.append(new_td("score", m_item));
            add_tr.append($("<td></td>"));
            add_tr.attr("id", main_tr_id + "_" + m_item["user_name"]);
            $("#t_mine").append(add_tr);
            add_tr.hide();
        }
    }
}


$(document).ready(function () {
    var url = location.pathname;
    var export_url = $("#export_url").val();
    var months = UrlArgsValue(location.href, "months");
    if(months == null){
        months = "";
    }
    export_url += "?months=" + months;
    var args = {"months": months};
    var multi = UrlArgsValue(location.href, "multi");
    if(multi != null){
        args["multi"] = multi;
        export_url += "&multi=" + multi;
    }
    $("#link_export").attr("href", export_url);
    my_async_request2(url, "GET", args, load_performance)
});
