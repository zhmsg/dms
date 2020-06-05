/**
 * Created by msg on 8/5/16.
 */

function UrlArgsValue(url, key)
{
    var reg = new RegExp("(&|^|\\?)" + key + "=([^&]*)(&|$)");
    var UrlValue = url.match(reg);
    if(UrlValue != null){
        return UrlValue[2];
    }
    return null;
}