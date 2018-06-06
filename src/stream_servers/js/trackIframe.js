// Not a part of jQuery on-mutate

var player_selector = [
    ".load-vid", // KickAssAnime
    "#load_anime" // GoGoAnime
];

function initiateTracker() {
    $(player_selector).onCreate('iframe', function (iframeElement) {
        console.log("iframe created");

        $(iframeElement).on('load', function () {
            var already_loaded = false
            updateIframeLoadStatus(1);
            console.log("iframe loaded");
        });
    });

    console.log("tracker running");
}

// Decide on a player selector
player_selector = player_selector.filter(selector => {
    return $(selector).length;
})[0];

initiateTracker();

