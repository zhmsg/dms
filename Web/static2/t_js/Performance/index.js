
function load_statistics(statistics) {
    var svg = d3.select("svg"),
            margin = {top: 20, right: 20, bottom: 30, left: 40},
            width = +svg.attr("width") - margin.left - margin.right,
            height = +svg.attr("height") - margin.top - margin.bottom,
            g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x0 = d3.scaleBand()
            .rangeRound([0, width])
            .paddingInner(0.1);

    var x1 = d3.scaleBand()
            .padding(0.05);

    var y = d3.scaleLinear()
            .rangeRound([height, 0]);

    var z = d3.scaleOrdinal()
            .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
    var data = statistics.data;
    var keys = statistics.columns;
    x0.domain(statistics.users);
    x1.domain(keys).rangeRound([0, x0.bandwidth()]);
    y.domain([0, d3.max(data, function (d) {
        return d3.max(keys, function (key) {
            return d[key];
        });
    })]).nice();

    g.append("g")
            .selectAll("g")
            .data(data)
            .enter().append("g")
            .attr("transform", function (d) {
                return "translate(" + x0(d.State) + ",0)";
            })
            .selectAll("rect")
            .data(function (d) {
                return keys.map(function (key) {
                    return {key: key, value: d[key]};
                });
            })
            .enter().append("rect")
            .attr("x", function (d) {
                return x1(d.key);
            })
            .attr("y", function (d) {
                return y(d.value);
            })
            .attr("width", x1.bandwidth())
            .attr("height", function (d) {
                return height - y(d.value);
            })
            .attr("fill", function (d) {
                return z(d.key);
            });

    g.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x0));

    g.append("g")
            .attr("class", "axis")
            .call(d3.axisLeft(y).ticks(null, "s"))
            .append("text")
            .attr("x", 2)
            .attr("y", y(y.ticks().pop()) + 0.5)
            .attr("dy", "0.32em")
            .attr("fill", "#000")
            .attr("font-weight", "bold")
            .attr("text-anchor", "start")
            .text("Population");

    var legend = g.append("g")
            .attr("font-family", "sans-serif")
            .attr("font-size", 10)
            .attr("text-anchor", "end")
            .selectAll("g")
            .data(keys.slice().reverse())
            .enter().append("g")
            .attr("transform", function (d, i) {
                return "translate(0," + i * 20 + ")";
            });

    legend.append("rect")
            .attr("x", width - 19)
            .attr("width", 19)
            .attr("height", 19)
            .attr("fill", z);

    legend.append("text")
            .attr("x", width - 24)
            .attr("y", 9.5)
            .attr("dy", "0.32em")
            .text(function (d) {
                return d;
            });
}
function load_keys(data) {
    var current_user = $("#current_user_name").val();

    var pr_items = data["detail"];
    var statistics = data["statistics"];

    load_statistics(statistics);
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
