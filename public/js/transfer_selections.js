var confirmedSources = document.getElementById('selections');
var unconfirmedSources = document.getElementById('sources');
var moveToConfirmedButton = document.getElementById('right');
var moveToUnconfirmedButton = document.getElementById('left');

function getSelectValues(selectField) {
    var result = [];
    var options = selectField.options;
    var opt;

    for (var i=0; i < options.length; i++){
        opt = options[i];
        if (opt.selected) {
            result.push({"value": opt.value, "innerHTML": opt.innerHTML, "index": i});
        }
    }
    return result;
}

function confirmSelections() {
    var selections = getSelectValues(unconfirmedSources);
    // loop from the back so index numbers work for removal
    for (var i = selections.length - 1; i >= 0; i--) {
        item = selections[i];
        unconfirmedSources.remove(item['index']);
        var newOption = document.createElement('option');
        newOption.value = item['value'];
        newOption.innerHTML = item['innerHTML'];
        confirmedSources.appendChild(newOption);
    }
}

function unconfirmSelections() {
    var selections = getSelectValues(confirmedSources);
    // loop from the back so index numbers work for removal
    for (var i = selections.length - 1; i >= 0; i--) {
        item = selections[i];
        confirmedSources.remove(item['index']);
        var newOption = document.createElement('option');
        newOption.value = item['value'];
        newOption.innerHTML = item['innerHTML'];
        unconfirmedSources.appendChild(newOption);
    }

}

moveToConfirmedButton.addEventListener('click', confirmSelections);
moveToUnconfirmedButton.addEventListener('click', unconfirmSelections);
