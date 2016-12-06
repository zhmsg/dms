/**
 * Created by msg on 12/6/16.
 */

function calc_result(data){
    console.info(data);
}

$(document).ready(function () {
    $("#reset").click(function () {
        $("input").val("");
    });
    $("input").keyup(function () {
        var v = this.value;
        v = v.replace(/([^\d\.]*)/g, "");
        this.value = v;
    });
    $("#calc").click(function () {
        $("#zhishu").text("");
        $("#kenengxing").text("");
        var mul_input = $("input");
        var calc_data = new Object();
        for (var i = 0; i < mul_input.length; i++) {
            var input_item = $(mul_input[i]);
            var item_id = input_item.attr("id");
            var item_v = parseFloat(input_item.val());
            if (isNaN(item_v)) {
                input_item.select();
                return false;
            }
            input_item.val(item_v);
            calc_data[item_id] = item_v;
        }
        var zhishu = 0.15939858 * calc_data["max_shibihoudu"] - 0.00294271 * calc_data["max_shibihoudu"] * calc_data["max_shibihoudu"] + 0.0259082 * calc_data["zuofangneijing"] + 0.00446131 * calc_data["yalijiecha"] + 0.4583082 * calc_data["cusijiazushi"] + 0.82639195 * calc_data["nsvt"] + 0.71650361 * calc_data["hunjue"] - 0.01799934 * calc_data["age"];
        calc_data["zhishu"] = zhishu;
        $("#zhishu").text(zhishu);
        var kenengxing = 1 - Math.pow(0.998, Math.pow(Math.E, zhishu));
        calc_data["kenengxing"] = kenengxing;
        $("#kenengxing").text(kenengxing);
        my_async_request2(location.href, "POST", calc_data, calc_result);
    });
});