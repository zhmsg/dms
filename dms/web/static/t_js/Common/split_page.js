/**
 * Created by msg on 3/15/17.
 */


function force_current_page(total_page, current_page, show_num) {
    var page_count = parseInt(total_page);
    var u = $("#pagination");
    u.find("li").remove();
    var start_num = 1;
    var end_num = page_count;
    if (show_num == null) {
        show_num = 15;
    }
    var mid_num = parseInt((show_num + 1) / 2);
    var left_num = show_num - mid_num;
    if (current_page <= mid_num) {
        if (page_count > show_num) {
            end_num = show_num;
        }
    }
    else if (page_count - current_page < left_num) {
        if (page_count > show_num) {
            start_num = page_count - show_num + 1;
        }
    }
    else {
        start_num = current_page - left_num;
        end_num = start_num + show_num - 1;
    }
    for (var i = start_num; i <= end_num; i++) {
        if (i == current_page) {
            u.append('<li class="active" id=li_page_' + i + '><a href="javascript:void(0)">' + i + '</a></li>');
        }
        else {
            u.append('<li id=li_page_' + i + '><a href="javascript:void(0)">' + i + '</a></li>');
        }
    }
    $("li[id^='li_page_']").click(function () {
        var page_num = parseInt(this.id.substr(8));
        search_code(page_num);
    });
}