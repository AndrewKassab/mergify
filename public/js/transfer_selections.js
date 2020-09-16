var confirmedSources = document.getElementById('sources');
var unconfirmedSources = document.getElementById('selections');
var moveToConfirmedButton = document.getElementById('right');
var moveToUnconfirmedButton = document.getElementById('left');

function confirmSelections() {
    // TODO: Move each selected item in unconfirmedSources into confirmedSources
}

function unconfirmSelections() {
    // TODO: Move each selected item in confirmedSources into unconfirmedSources
}

moveToConfirmedButton.addEventListener('click', confirmSelections);
moveToUnconfirmedButton.addEventListener('click', unconfirmSelections);
