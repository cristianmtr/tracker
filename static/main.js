var dataSet;

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
