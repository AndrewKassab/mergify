let sourceSelections = document.getElementById('selections');
let destDataList = document.getElementById('destination_playlists');
let mergeButton = document.getElementById('confirm');
let destinationInput = document.getElementById('destination_selection');

var request = new XMLHttpRequest();

request.onreadystatechange = function() {
    if (this.readyState == XMLHttpRequest.DONE) {
        if (xhr.status != 201) {
            // TODO: error handle
        }
        // TODO: Otherwise, output success
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
    var data = {};
    var error = false;
    var isNewPlaylist = false;
    var destinationPlaylist = destinationInput.value;
    var sourcePlaylists = getSelectedSources();

    if (!destinationPlaylist) {
        // TODO Handle missing destination error
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
        // TODO: Handle missing sources error
    }

    if (error) {
        return; // Abandon call due to errors
    }

    data['source_playlists'] = sourcePlaylists;
    data['destination_playlist'] = destinationPlaylist;
    data['to_new'] = isNewPlaylist;

    // TODO: Display some loading / timed modal that dissapears once the request is done
    request.open('POST', 'http://localhost:5000/merge');
    request.withCredentials = true; // TODO: DEV ONLY
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(data));
}

mergeButton.addEventListener('click', merge);