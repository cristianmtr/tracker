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

    $('#deadline').editable({
        type: 'combodate',
	format: 'DD.MM.YYYY',
	title: 'Deadline',
        viewformat: 'DD.MMMM.YYYY',    
        template: 'DD.MMMM.YYYY',
	value: moment().format(new moment().format("DD.MM.YYYY")),
        combodate: {
                minYear: 2015,
                maxYear: 2016,
                minuteStep: 1
           }
	
    })


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
