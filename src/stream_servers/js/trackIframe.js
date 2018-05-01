player_selector = ".load-vid"

function updateLoadStatus(status) {
    load_status = {
        iframe_loaded: status
    };

    $("#load_status").html(JSON.stringify(load_status));
}

function createElement() {
    var element = document.createElement('div');
    element.id = "load_status";
    document.body.appendChild(element);
    updateLoadStatus(0);
}

function initiateTracker() {
    $(player_selector).onCreate('iframe', function (iframeElement) {
        console.log("iframe created");

        $(iframeElement).on('load', function () {
            already_loaded = false
            updateLoadStatus(1);
            console.log("iframe loaded");
        });
    });

    console.log("tracker running");
}



(function () {
    createElement();
    initiateTracker();
})();


