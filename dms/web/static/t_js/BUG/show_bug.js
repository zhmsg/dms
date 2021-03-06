/**
 * Created by meisanggou on 17-03-01.
 */

bug_level_desc = [];

function drawBar(data, father_id, bar_name) {
    //默认svg 图中上下左右有空白宽度为50px
    var topPadding = 50;
    var botttomPadding = 100;
    var leftPaddding = 50;
    var rightPadding = 50;
    var xSpace = 80;
    var xWidth = data.length * xSpace;
    var yHeight = 500;
    var dataX = [];
    var dataY = [];
    for (var i = 0; i < data.length; i++) {
        dataX.push(data[i].nick_name);
        dataY.push(data[i].bug_num);
    }
    console.log("dataX", dataX);
    console.log("dataY", dataY);
    d3.select("#" + father_id).selectAll("svg").remove();
    var svg = d3.select("#" + father_id)
        .append("svg")
        .attr("width", leftPaddding + xWidth + rightPadding)
        .attr("height", topPadding + yHeight + botttomPadding);

    var xAxisScale = d3.scale.ordinal()//x�����
        .domain(dataX)
        .rangeRoundBands([0, xWidth]);

    var yAxisScale = d3.scale.linear()
        .domain([0, d3.max(dataY) + 10])
        .range([yHeight, 0]);

    var xScale = d3.scale.ordinal()// ����һ���������ߡ�x������
        .domain(d3.range(dataX.length))
        .rangeRoundBands([0, xWidth], 0.05);

    var yScale = d3.scale.linear()// ����һ�����Զ�������ߡ�
        .domain([0, d3.max(dataY) + 10])
        .range([0, yHeight]);

    var xAxis = d3.svg.axis()
        .scale(xAxisScale)
        .orient("bottom");

    var yAxis = d3.svg.axis()// ����һ��axis�������
        .scale(yAxisScale)
        .orient("left");

    svg.selectAll("rect")
        .data(dataY)
        .enter()
        .append("rect")
        .attr("x", function (d, i) {
            return leftPaddding + xScale(i);
        })
        .attr("y", function (d, i) {
            return topPadding + yHeight - yScale(d);
        })
        .attr("width", function (d, i) {
            return xScale.rangeBand();
        })
        .attr("height", function (d, i) {
            return yScale(d);
        })
        .attr("fill", "pink");

    svg.selectAll("text")
        .data(dataY)
        .enter()
        .append("text")
        .attr("x", function (d, i) {
            return leftPaddding + xSpace * (i + 0.5);//~= leftPaddding + xScale(i) + xSpace/2
        })
        .attr("y", function (d, i) {
            return topPadding + yHeight - yScale(d) - 5;
        })
        .attr("font-size", 15)
        .attr("fill", "black")
        .text(function (d, i) {
            return d;
        });

    svg.append("g")
        .attr("class", "axis")
        .attr("fill", "gray")
        .attr("transform", "translate(" + leftPaddding + "," + (topPadding + yHeight) + ")")
        .call(xAxis)
        .append("g")
    ;

    svg.append("g")
        .attr("class", "axis")
        .attr("fill", "gray")
        .attr("transform", "translate(" + leftPaddding + "," + topPadding + ")")
        .call(yAxis);

    svg.append("text")
        .attr("x", leftPaddding + xWidth / 2)
        .attr("y", topPadding + yHeight + botttomPadding / 1.5)
        .attr("font-size", 18)
        .attr("fill", "black")
        .text(bar_name);
}

function jump_detail() {
    var parent_tr = $(this).parent().parent();
    var bug_no = parent_tr.attr("id").substr(3);
    location.href = $("#info_url").val() + "?bug_no=" + bug_no;
}

function handler_level() {
    var td_level = $(this);
    var level_val = parseInt(td_level.text());
    var td_class = "";
    var td_text = level_val;
    if (level_val > bug_level_desc.length) {
        td_text = "内部异常";
    }
    else {
        td_text = bug_level_desc[level_val];
    }
    td_level.text(td_text);
}


function handle_bug_list(bug_list) {
    var t_id = "t_wait_solve";
    var t = $("#" + t_id);
    var len_list = bug_list.length;
    if(len_list == 0){
        var add_tr = $("<tr></tr>");
        var add_td = $("<td>暂无未解决的问题</td>");
        add_td.attr("colSpan", "6");
        add_td.addClass("redColor");
        add_tr.append(add_td);
        t.append(add_tr);
    }
    var keys = ["bug_title", "bug_status", "submitter", "submit_time", "bug_level"];
    for (var i = 0; i < len_list; i++) {
        var bug_item = bug_list[i];
        var add_tr = $("<tr id='tr_" + bug_item["bug_no"] + "'></tr>");
        for (var j = 0; j < keys.length; j++) {
            add_tr.append(new_td(keys[j], bug_item));
        }
        add_tr.append($('<td><a name="look_detail1" href="javascript:void(0)">查看</a></td>'));
        t.append(add_tr);
    }
    var bug_status_desc = JSON.parse($("#bug_status_desc").text());
    $("td[name='td_bug_status']").each(function () {
        var td_status = $(this);
        var status_val = td_status.text();
        var td_class = "";
        var td_text = status_val;
        switch (status_val) {
            case "0":
                td_class = "redBg";
                td_text = bug_status_desc[0];
                break;
            case "1":
                td_class = "orgBg";
                td_text = bug_status_desc[1];
                break;
            case "2":
                td_class = "yellowBg";
                td_text = bug_status_desc[2];
                break;
            case "3":
                td_class = "greenBg";
                td_text = bug_status_desc[3];
                break;
            default:
                td_text = "内部异常";
        }
        td_status.addClass(td_class);
        td_status.text(td_text);
    });
    $("td[name='td_bug_level']").each(handler_level);
    $("a[name='look_detail1']").click(jump_detail);
}


function handle_my_bug(bug_list) {
    var t_id = "t_my_bug";
    var t = $("#" + t_id);
    var len_list = bug_list.length;
    if(len_list == 0){
        var add_tr = $("<tr></tr>");
        var add_td = $("<td>还没有属于自己的问题</td>");
        add_td.attr("colSpan", "5");
        add_td.addClass("redColor");
        add_tr.append(add_td);
        t.append(add_tr);
    }
    var keys = ["bug_title", "submitter", "submit_time", "bug_level"];
    for (var i = 0; i < len_list; i++) {
        var bug_item = bug_list[i];
        var add_tr = $("<tr id='tr_" + bug_item["bug_no"] + "'></tr>");
        for (var j = 0; j < keys.length; j++) {
            add_tr.append(new_td(keys[j], bug_item));
        }
        add_tr.append($('<td><a name="look_detail2" href="javascript:void(0)">查看</a></td>'));
        t.append(add_tr);
    }
    $("td[name='td_bug_level']").each(handler_level);
    $("a[name='look_detail2']").click(jump_detail);
}


function submit_problem() {
    var bug_title = $("input[name='bug_title']").val();
    var bug_level = $("#select_bug_level").val();
    var bug_level_desc = $("#select_bug_level").find("option:selected").text();
    var swal_text = "[" + bug_level_desc + "]" + bug_title;
    swal({
            title: "确定提交",
            text: swal_text,
            type: "info",
            showCancelButton: true,
            confirmButtonColor: '#DD6B55',
            confirmButtonText: '提交',
            cancelButtonText: "取消",
            closeOnConfirm: true,
            closeOnCancel: true
        },
        function (isConfirm) {
            if (isConfirm) {
                var request_url = location.href;
                my_async_request2(request_url, "POST", {"bug_title": bug_title, "bug_level": parseInt(bug_level)});
            }
        }
    );
}

$(function () {
    //var bug_statistic_url = $("#bug_statistic_url").val();
    //$.ajax({
    //    url: bug_statistic_url,
    //    method:"GET",
    //    success:function(data){
    //        console.log("get statistic :",data);
    //        if(data.status){
    //            drawBar(data.data.month,"bar_month","月统计图");
    //            drawBar(data.data.all,"bar_all","总统计图");
    //        }else{
    //            alert("内部错误:获取统计数据失败");
    //        }
    //    },
    //    error:function(){
    //        alert("网络错误:获取统计数据失败");
    //    }
    //});
    var bug_url = location.href;
    my_async_request2(bug_url, "GET", null, handle_bug_list);
    bug_level_desc = JSON.parse($("#bug_level_desc").text());
    var current_user_role = parseInt($("#current_user_role").val());
    var new_link_role = $("#new_link_role").val().split("|");
    var bit_new = current_user_role & parseInt(new_link_role[0]);
    var bit_link = current_user_role & parseInt(new_link_role[1]);
    if (bit_new > 0) {
        $("#div_add_problem").show();
        var index = 1;
        if (bit_link > 0)
            index = 0;
        for (; index < bug_level_desc.length; index++) {
            add_option("select_bug_level", index, bug_level_desc[index]);
        }
        // 自动保存和加载选择的项
        var storage_key = "dms_select_bug_level";
        var s_value = localStorage.getItem(storage_key);
        if (s_value != null) {
            $("#select_bug_level").val(s_value);
        }
        $("#select_bug_level").change(function () {
            localStorage.setItem(storage_key, $("#select_bug_level").val());
        });
        $("#btn_submit_problem").click(submit_problem);
    }
    if(bit_link <= 0){
        $("#btn_jy_mine").hide();
        $("#btn_jy_wait_solve").click();
    }
    else{
        var my_bug_url = $("#my_bug_url").val();
        my_async_request2(my_bug_url, "GET", null, handle_my_bug);
    }
});
