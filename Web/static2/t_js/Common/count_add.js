/**
 * Created by msg on 5/31/16.
 */

$(function(){
    $("a").click(function(){
        var next_url = this.href;
        var match_next = next_url.match(/(http:\/\/|https:)?(\S*?)\//i);
        if(match_next == null){
            return;
        }
        var next_host = match_next[2];
        if(next_host != location.host){
            alert(next_host);
        }
        var request_data = new Object();
        request_data["destination_info"] = next_url;
        my_request("http://ih.gene.ac/api/v2/ad/?geneacdms=test", "POST", request_data, null);
    });

});
