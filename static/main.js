var dataSet;

var modalDataSet = [
    ["deadline", "2more"],
    ["responsible", "you!"],
]

function insertNewRow(listObject) {
    var table = document.getElementById("modaltable");
    var row = table.insertRow(0);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = listObject[0];
    cell2.innerHTML = listObject[1];
}

function insertNewRowEmpty() {
    var table = document.getElementById("modaltable");
    var row = table.insertRow(0);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = "deadline";
    cell2.innerHTML = "2more";
    return;
}

$(document).ready(function () {

    function test() {
        return $.getJSON('/json');
    }

    $.when(test()).then(function (data) {
        dataSet = data['data'];
        $('#example').DataTable({
            "data": dataSet,
            "columns": [{
                "title": "id"
            }, {
                "title": "description"
            }, {
                "title": "dead line"
            }, {
                "title": "responsible"
            }, {
                "title": "author"
            }]
        });
    });



});
