var load_status = {
    document_loaded: 0,
    iframe_loaded: 0
};

function updateDocumentLoadStatus(status) {
    load_status = JSON.parse($("#load_status").html());
    load_status.document_loaded = status;
    $("#load_status").html(JSON.stringify(load_status));
}

function updateIframeLoadStatus(status) {
    load_status = JSON.parse($("#load_status").html());
    load_status.iframe_loaded = status;
    $("#load_status").html(JSON.stringify(load_status));
}

function createElement() {
    var element = document.createElement('div');
    element.id = "load_status";
    element.innerHTML = JSON.stringify(load_status);
    document.body.appendChild(element);
}

createElement();

$(document).ready(function(){
    updateDocumentLoadStatus(1);
});