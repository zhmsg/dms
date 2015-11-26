/**
 * Created by lsl on 15-11-26.
 */
<!--上传vcf START-->
function fileSelected() {
    var file = document.getElementById('selectB').files[0];
    if (file) {
        var fileSize = 0;
        if (file.size > 1024 * 1024)
            fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
        else
            fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';
        document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
        document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
        //document.getElementById('progressNumber').innerHTML = '0%';
    }
}
function uploadFile() {
    var fd = new FormData();
    fd.append("file", document.getElementById('selectB').files[0]);
    //fd.append("csrf_token", document.querySelector('meta[name="csrf-token"]').getAttribute('content'));
    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener("progress", uploadProgress, false);
    xhr.addEventListener("load", uploadComplete, false);
    xhr.addEventListener("error", uploadFailed, false);
    xhr.addEventListener("abort", uploadCanceled, false);
    xhr.open("POST", "/dev/bug/upload/");
    xhr.send(fd);
    $("#upB").hide();
    $("#selectB").hide();
}
function uploadProgress(evt) {
    if (evt.lengthComputable) {
        var percentComplete = Math.round(evt.loaded * 100 / evt.total);
        document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
    }
    else {
        document.getElementById('progressNumber').innerHTML = 'unable to compute';
    }
}
function uploadComplete(evt) {
    /* This event is raised when the server send back a response */
    alert(this.responseText);
    $("#message").show();
    $("#up_vcf").attr("disabled","disabled");
    $("#up_vcf").removeClass("btn-primary");
}
function uploadFailed(evt) {
    alert(this.responseText);
}
function uploadCanceled(evt) {
    alert("The upload has been canceled by the user or the browser dropped the connection.");
}
<!--上传vcf END-->