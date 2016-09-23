/**
 * Created by msg on 9/23/16.
 */

function clear_input_value()
{
    $("input").val("");
    $("textarea").val("");
}

$(function() {
    $("#a_popup").click(clear_input_value);
});