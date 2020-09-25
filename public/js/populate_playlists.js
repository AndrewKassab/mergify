let sourceSelectField = document.getElementById('sources');
let destinationDataList = document.getElementById('destination_playlists');

let xhr = new XMLHttpRequest();

xhr.onreadystatechange = function() {
    if (this.readyState == XMLHttpRequest.DONE){
        // TODO: Error handling on page, output message / redirect to login?
        if (xhr.status != 200) {
            return;
        }
        var response = JSON.parse(this.responseText);
        for (var key in response){
            let newOption = document.createElement('option');
            newOption.value = key;
            newOption.innerHTML = response[key];
            sourceSelectField.appendChild(newOption);
            destinationDataList.appendChild(newOption); // TODO: May need to clone
        }
    }
}

xhr.open('GET', 'http://localhost:5000/playlists');
xhr.withCredentials = true; // TODO: DEV ONLY
xhr.send();
