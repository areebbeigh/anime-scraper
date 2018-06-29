// Not a part of jQuery on-mutate

var player_selector = [
    ".load-vid", // KickAssAnime
    "#load_anime" // GoGoAnime
];

function initiateTracker() {
    // $(player_selector).onCreate('iframe', function (iframeElement) {
    //     alert("iframe created");

    // });

    let mutationObserver = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            let element = mutation.target;
            let iframe = $(element);

            if (element.tagName != "IFRAME")
                iframe = $(element).find("iframe");           

            iframe.on('load', function () {
                var already_loaded = false
                updateIframeLoadStatus(1);
                console.log("iframe loaded");
            });

            console.log(mutation);
        });
    });

    mutationObserver.observe($(player_selector)[0], {
        childList: true,
        attributes: true,
        attributeOldValue: true,
        subtree: true,
    });

    console.log("tracker running");
}

// Decide on a player selector
player_selector = player_selector.filter(selector => {
    return $(selector).length;
})[0];

initiateTracker();