/**
 * Created by lsl on 15-11-25.
 */
$(function(){
    $.ajax({
        url:"/dev/bug/statistic/",
        method:"GET",
        success:function(data){
            console.log("get statistic :",data);
            if(data.status){
                draw(data.data);
            }else{
                alert("内部错误:获取统计数据失败");
            }
        },
        error:function(){
            alert("网络错误:获取统计数据失败");
        }
    });
});
function draw(data){
    drawBar(data.month,"bar_month","月统计图");
    drawBar(data.all,"bar_all","总统计图");
}
function drawBar(data,father_id,bar_name){
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
        .attr("width",700)
        .attr("height",700);

    var xAxisScale = d3.scale.ordinal()//x�����
        .domain(dataX)
        .rangeRoundBands([0,dataX.length*80]);

    var yAxisScale = d3.scale.linear()
        .domain([0,d3.max(dataY)+10])
        .range([500,0]);

    var xScale = d3.scale.ordinal()// ����һ���������ߡ�x������
        .domain(d3.range(dataX.length))
        .rangeRoundBands([0,dataX.length*80],0.1);

    var yScale = d3.scale.linear()// ����һ�����Զ�������ߡ�
        .domain([0,d3.max(dataY)+10])
        .range([0,500]);

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
            return 40+ xScale(i);
        } )
        .attr("y",function(d,i){
            return 50 + 550 - yScale(d) ;
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
            return 73 + xScale(i);
        } )
        .attr("y",function(d,i){
            return 95+500 - yScale(d) ;
        })
        .attr("font-size", 10)
        .attr("fill","black")
        .text(function(d,i){
            return d;
        });

    svg.selectAll("text")
        .data(dataX)
        .enter()
        .append("text")
        .attr("x", function(d,i){
            return 73 + xScale(i);
        } )
        .attr("y",function(d,i){
            return 95+500  ;
        })
        .attr("font-size", 25)
        .attr("fill","red")
        .text("I");

    svg.append("g")
        .attr("class","axis")
        .attr("fill","gray")
        .attr("transform","translate(40,601)")
        .call(xAxis)
        .append("g")
    ;

    svg.append("g")
        .attr("class","axis")
        .attr("fill","gray")
        .attr("transform","translate(40,100)")
        .call(yAxis);

    svg.append("text")
        .attr("x",350)
        .attr("y",680)
        .attr("font-size", 18)
        .attr("fill","black")
        .text(bar_name);
}