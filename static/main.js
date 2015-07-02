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

    $.fn.editable.defaults.mode = 'inline';

    $('#priority').editable({
        type: 'select',
        title: 'Priority',
        placement: 'right',
        value: 2,
        source: [
            {value: 1, text: 'Urgent'},
            {value: 2, text: 'Medium'},
            {value: 3, text: 'Low'}
        ]

    });

    $('#tasklist').editable({
        type: 'select',
        title: 'Task list',
        placement: 'right',
        value: 3,
        source: [
            {value: 1, text: 'Dummy'},
            {value: 2, text: 'Fake'},
            {value: 3, text: 'Foo'},
            {value: 4, text: 'Bar'},
        ]
    });

    $("#title").editable({
        type: 'text',
        title: 'Title',
        clear: true,
        placeholder: 'task title',
    });

    $("#description").editable({
        type: 'textarea',
        escape: true,
    });

    $("#responsible").editable({
        type: 'select',
        value: 1,
        title: 'Responsible',
        placement: 'right',
        source: [
            {value: 1, text: 'Cristian'},
            {value: 2, text: 'Someone else'},
        ]
    });

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
