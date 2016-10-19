/**
 * Created by lsl on 15-11-25.
 */
$(function(){
    var bug_statistic_url = $("#bug_statistic_url").val();
    $.ajax({
        url: bug_statistic_url,
        method:"GET",
        success:function(data){
            console.log("get statistic :",data);
            if(data.status){
                drawBar(data.data.month,"bar_month","月统计图");
                drawBar(data.data.all,"bar_all","总统计图");
            }else{
                alert("内部错误:获取统计数据失败");
            }
        },
        error:function(){
            alert("网络错误:获取统计数据失败");
        }
    });
});
function drawBar(data,father_id,bar_name){
    //默认svg 图中上下左右有空白宽度为50px
    var topPadding=50;
    var botttomPadding=100;
    var leftPaddding=50;
    var rightPadding=50;
    var xSpace=80;
    var xWidth=data.length*xSpace;
    var yHeight=500;
    var dataX=[];
    var dataY=[];
    for(var i=0;i<data.length;i++){
        dataX.push(data[i].nick_name);
        dataY.push(data[i].bug_num);
    }
    console.log("dataX",dataX);
    console.log("dataY",dataY);
    d3.select("#"+father_id).selectAll("svg").remove();
    var svg = d3.select("#"+father_id)
        .append("svg")
        .attr("width",leftPaddding+xWidth+rightPadding)
        .attr("height",topPadding+yHeight+botttomPadding);

    var xAxisScale = d3.scale.ordinal()//x�����
        .domain(dataX)
        .rangeRoundBands([0,xWidth]);

    var yAxisScale = d3.scale.linear()
        .domain([0,d3.max(dataY)+10])
        .range([yHeight,0]);

    var xScale = d3.scale.ordinal()// ����һ���������ߡ�x������
        .domain(d3.range(dataX.length))
        .rangeRoundBands([0,xWidth],0.05);

    var yScale = d3.scale.linear()// ����һ�����Զ�������ߡ�
        .domain([0,d3.max(dataY)+10])
        .range([0,yHeight]);

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
        .attr("x", function(d,i){
            return leftPaddding+ xScale(i);
        } )
        .attr("y",function(d,i){
            return topPadding + yHeight - yScale(d) ;
        })
        .attr("width", function(d,i){
            return xScale.rangeBand();
        })
        .attr("height",function(d,i){
            return yScale(d);
        })
        .attr("fill","pink");

    svg.selectAll("text")
        .data(dataY)
        .enter()
        .append("text")
        .attr("x", function(d,i){
            return leftPaddding  + xSpace*(i+0.5) ;//~= leftPaddding + xScale(i) + xSpace/2
        } )
        .attr("y",function(d,i){
            return topPadding + yHeight - yScale(d) -5;
        })
        .attr("font-size", 15)
        .attr("fill","black")
        .text(function(d,i){
            return d;
        });

    svg.append("g")
        .attr("class","axis")
        .attr("fill","gray")
        .attr("transform","translate("+leftPaddding+","+(topPadding+yHeight)+")")
        .call(xAxis)
        .append("g")
    ;

    svg.append("g")
        .attr("class","axis")
        .attr("fill","gray")
        .attr("transform","translate("+leftPaddding+","+topPadding+")")
        .call(yAxis);

    svg.append("text")
        .attr("x",leftPaddding+xWidth/2)
        .attr("y",topPadding+yHeight+botttomPadding/1.5)
        .attr("font-size", 18)
        .attr("fill","black")
        .text(bar_name);
}