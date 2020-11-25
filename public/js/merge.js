let sourceSelections = document.getElementById('selections');
let destDataList = document.getElementById('destination_playlists');
let mergeButton = document.getElementById('confirm');
let destinationInput = document.getElementById('destination_selection');
let noDestError = document.getElementById('no_dest_err');
let noSrcError = document.getElementById('no_src_err');
let loadmodal = document.getElementById('modal');
let loadWheel = document.getElementById('loader');
let modalSuccessMessage = document.getElementById('success_message');
let failedMergeError = document.getElementById('merge_error');
let pleaseWaitMessage = document.getElementById('pleasewait');
let closeButton = document.getElementById('closemodal');

var request = new XMLHttpRequest();

request.onreadystatechange = function() {
    if (this.readyState == XMLHttpRequest.DONE) {
        loadWheel.style.display = "none";
        closeButton.style.display = "";
        pleaseWaitMessage.style.display = "none";
        if (request.status == 201) {
            modalSuccessMessage.style.display = "";
        } else {
            failedMergeError.style.display = "";
        }
    }
}

function getSelectedSources() {
    var result = [];
    var options = sourceSelections.options; 
    for (var i = 0; i < options.length; i++) {
        result.push(options[i].value);
    }
    return result;
}

function getMatchingOptionData(playlistName) {
    var options = destDataList.options;
    for (var i = 0; i < options.length; i++) {
        option = options[i];
        if (option.innerHTML == playlistName) {
            return option.getAttribute('data');
        }
    }
    return playlistName;
}

function merge() {
    noDestError.style.display = "none";
    noSrcError.style.display = "none";

    var data = {};
    var error = false;
    var isNewPlaylist = false;
    var destinationPlaylist = destinationInput.value;
    var sourcePlaylists = getSelectedSources();

    if (!destinationPlaylist) {
        noDestError.style.display = "";
        error = true;
    } else {
        var id = getMatchingOptionData(destinationPlaylist);
        if (id == destinationPlaylist) {
            isNewPlaylist = true;
        } else {
            destinationPlaylist = id;
        }
    }

    if (sourcePlaylists.length == 0) {
        error = true;
        noSrcError.style.display = "";
    }

    if (error) {
        return; // Abandon call due to errors
    }

    data['source_playlists'] = sourcePlaylists;
    data['destination_playlist'] = destinationPlaylist;
    data['to_new'] = isNewPlaylist;

    request.open('POST', 'http://localhost:5000/merge');
    request.withCredentials = true; // TODO: DEV ONLY
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(data));
    modal.style.display = "";
}

mergeButton.addEventListener('click', merge);
closeButton.addEventListener('click', () => {
    modal.style.display = "none";
    location.reload();
});
