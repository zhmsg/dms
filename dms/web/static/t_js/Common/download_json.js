/**
 * Created by msg on 6/16/16.
 */


function DownloadJson(filename,content)
{
    var download_a = document.createElement('a');
    download_a.download = filename;
    download_a.href = "data:application/json;charset=utf-8," + encodeURIComponent(content);
    //document.body.appendChild(download_a);
    download_a.click();
    //document.body.removeChild(download_a);
}

function DownloadFile(fileName, content)
{
    var download_a = document.createElement('a');
    var blob = new Blob([content]);
    //var evt = document.createEvent("HTMLEvents");
    //evt.initEvent("click", false, false);//initEvent 不加后两个参数在FF下会报错
    download_a.download = fileName;
    console.info("here");
    download_a.href = URL.createObjectURL(blob);
    console.info("there");
    //download_a.dispatchEvent(evt);
    document.body.appendChild(download_a);
    download_a.click();
    document.body.removeChild(download_a);
}