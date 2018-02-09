
function load_keys(data) {
    var current_user = $("#current_user_name").val();

    var pr_items = data["detail"];
    var statistics = data["statistics"];

    draw_stacked_bar_chart("#svg_total", statistics.columns, statistics.data);
    draw_bar_chart("#svg_1", statistics.data, "State", "技术");
    var pr_len = pr_items.length;

    var keys = ["month", "module_no", "name", "start_time", "end_time", "user_name", "score", "detail_info"];
    for(var i=0; i<pr_len; i++){
        var pr_item = pr_items[i];
        for(var j=0; j<pr_item.members.length; j++){
            var prm_item = $.extend({}, pr_item, pr_item.members[j]);
            prm_item["score"] = prm_item["score"] / 1000;
            prm_item["start_time"] = timestamp_2_date(pr_item["start_time"]);
            prm_item["end_time"] = timestamp_2_date(pr_item["end_time"]);
            var add_tr = $("<tr></tr>");
            for(var k=0; k<keys.length; k++){
                var td = new_td(keys[k], prm_item);
                add_tr.append(td);
            }
            $("#t_mine").append(add_tr);
        }
    }
}


$(document).ready(function () {
    var url = location.pathname;
    my_async_request2(url, "GET", {"data": true}, load_keys)
});
