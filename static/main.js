// TODO
const newItemForModal = {
    'title': '',
    'deadline' : new moment().format("YYYY-MM-DD"),
    'priority':2,
    'responsible':'',
    'description':'',
    'author':'',
    'tasklist':1,
}

function iterateDataSources() {
    for (var key in dataSources) {
	if (dataSources.hasOwnProperty(key)) {
	    console.log(key + " -> " + dataSources[key]);
	    var subobj = dataSources[key];
	    for (var subkey in subobj) {
		if (subobj.hasOwnProperty(subkey)) {
		    console.log(subkey + " -> " + subobj[subkey]);
		}
	    }
	}
    }
};

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

var currentItemId;

function updateCurrentItemId(e) {
    currentItemId = $(e).attr('id');
    console.log(currentItemId);
    $.ajax({
	url: '/json/'+currentItemId,
	async: true,
	dataType: 'json',
	success: function(dataList) {
	    dataList = dataList['data'];
	    console.log("got data from server: " + JSON.stringify(dataList));
	    setDataInModal(dataList);
	}
    });
};

function setDataInModal(modalDataObject) {
    $('#priority').editable('setValue',modalDataObject['priority']);
    $('#deadline').data("DateTimePicker").date(modalDataObject['deadline']);
    $('#tasklist').editable('setValue',modalDataObject['tasklist']);
    $('#title').editable('setValue',modalDataObject['title']);
    $('#description').editable('setValue',modalDataObject['description']);
    $('#responsible').editable('setValue',modalDataObject['responsible']);
    
    console.log('data modal has been updated with ' + JSON.stringify(modalDataObject));
};

function initializeEditablesWithDefaults(dataSources) {
    $.fn.editable.defaults.mode = 'inline';

    $('#priority').editable({
        type: 'select',
        title: 'Priority',
        placement: 'right',
        value: 2,
	source: dataSources['priority'],
    });

    $('#tasklist').editable({
        type: 'select',
        title: 'Task list',
        placement: 'right',
        value: 1,
	source: dataSources['tasklist'],
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
	source: dataSources['responsible'],
    });

};

$(document).ready(function () {

    // Setup - add a text input to each footer cell
    $('#example tfoot th').each( function () {
        var title = $('#example thead th').eq( $(this).index() ).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );

    function test() {
        return $.getJSON('/json');
    }

    $.when(test()).then(function (data) {
    	console.log('got data from /json');
        dataSet = data['data'];
    	dataSources = data['dataSources'];
	var table = $('#example').DataTable({
            "data": dataSet,
            "columns": [{
                "title": "title"
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
	
	// Apply the search
	table.columns().every( function () {
            var that = this;
	    
            $( 'input', this.footer() ).on( 'keyup change', function () {
		that
                    .search( this.value )
                    .draw();
            } );
	} );

	initializeEditablesWithDefaults(dataSources);
    } );
    
});
