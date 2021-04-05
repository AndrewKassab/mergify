let sourceSelectField = document.getElementById('sources');
let destinationDataList = document.getElementById('destination_playlists');

let xhr = new XMLHttpRequest();

// TODO: Some sort of page load while this request is completed

xhr.onreadystatechange = function() {
    if (this.readyState == XMLHttpRequest.DONE) {
        // TODO: Error handling on page, output message / redirect to login?
        if (xhr.status != 200) {
            return;
        }
        var response = JSON.parse(this.responseText);
        for (var key in response) {
            let newOptionSelect = document.createElement('option');
            newOptionSelect.value = key;
            newOptionSelect.innerHTML = response[key];
            sourceSelectField.appendChild(newOptionSelect);
            let newOptionDataList = document.createElement('option');
            newOptionDataList.setAttribute("data", key);
            newOptionDataList.innerHTML = response[key];
            destinationDataList.appendChild(newOptionDataList);
        }
    }
}

// TODO: Update to just grab current URL then add endpoint
xhr.open('GET', 'http://24.25.205.133/api/playlists');
xhr.send()
