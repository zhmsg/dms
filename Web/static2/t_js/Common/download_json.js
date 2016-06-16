/**
 * Created by msg on 6/16/16.
 */


function DownloadJson(filename,content)
{
    var download_a = document.createElement('a');
    download_a.download = filename;
    download_a.href = "data:application/json;charset=utf-8," + encodeURIComponent(content);
    document.body.appendChild(download_a);
    download_a.click();
    document.body.removeChild(download_a);
}