/**
 * Created by msg on 17-7-6.
 */

$(document).ready(function () {
    var current_url = location.pathname;
    var path = location.href.substr(location.protocol.length + 2 + location.host.length);
    console.info(path);
    if (path.length > 32) {

        $("#link_op_s").show();
    }
});