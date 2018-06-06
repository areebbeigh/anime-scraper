function updateLoadStatus(status) {
    var load_status = {
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

var base_url = 'https://' + document.domain + '/';
const EPISODE_CONTAINER_ID = 'episode_list';

function createEpisodesContainer() {
    var element = document.createElement('div');
    element.id = EPISODE_CONTAINER_ID;
    document.body.appendChild(element);
}

/**
 * Loads all episode lists synchronously
 */
function loadEpisodeList() {
    var episode_list_data = [];
    var selector = '#' + EPISODE_CONTAINER_ID;

    $(document).ready(function () {
        $('#episode_page a').toArray().forEach((item) => {
            var ep_start = $(item).attr('ep_start');
            var ep_end = $(item).attr('ep_end');

            var id = $('input#movie_id').val();
            var default_ep = $('input#default_ep').val();

            var url = base_url + '/load-list-episode?ep_start=' + ep_start + '&ep_end=' + ep_end + '&id=' + id + '&default_ep=' + default_ep;

            // $('#' + EPISODE_CONTAINER_ID).load(url);

            $.ajax({
                url: url,
                async: false,
                success: data => {
                    episode_list_data.push(data);
                    // $(selector).append(data);
                    // console.log(ep_start);
                }
            });

        });
    });

    $(selector).append(episode_list_data);
    // updateLoadStatus(1);
}

// createElement();
createEpisodesContainer();
loadEpisodeList();