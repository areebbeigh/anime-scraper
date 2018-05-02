// Not a part of jQuery on-mutate

function updateLoadStatus(status) {
    load_status = {
        document_loaded: status
    };

    $("#load_status").html(JSON.stringify(load_status));
}

function createElement() {
    var element = document.createElement('div');
    element.id = "load_status";
    document.body.appendChild(element);
    updateLoadStatus(0);
}

(function main() {
    createElement();

    $(document).ready(function(){
        updateLoadStatus(1);
    });
})();
