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

var globalDataSources;

function iterateDataSources() {
    for (var key in globalDataSources) {
	if (globalDataSources.hasOwnProperty(key)) {
	    console.log(key + " -> " + globalDataSources[key]);
	    var subobj = globalDataSources[key];
	    for (var subkey in subobj) {
		if (subobj.hasOwnProperty(subkey)) {
		    console.log(subkey + " -> " + subobj[subkey]);
		}
	    }
	}
    }
};

function updateCurrentItemId(e) {
    var currentItemId = $(e).attr('id');
    console.log(currentItemId);
    $.ajax({
	url: '/json/'+currentItemId,
	async: true,
	dataType: 'json',
	success: function(modalDataObject) {
	    modalDataObject = modalDataObject['data'];
	    console.log("got data from server: " + JSON.stringify(modalDataObject));
	    setDataInModal(modalDataObject);
	}
    });
};

function setDataInModal(modalDataObject) {
    $('#priority').editable('setValue',modalDataObject['priority']);
    $('#deadline').data("DateTimePicker").date(modalDataObject['deadline']);
    $('#tasklist').editable('setValue',modalDataObject['tasklist']);
    $('#title').editable('setValue',modalDataObject['title']);
    $('#description').val(modalDataObject['description']);
    $('#responsible').editable('setValue',modalDataObject['responsible']);
    
    console.log('data modal has been updated with ' + JSON.stringify(modalDataObject));
};

function initializeEditables() {
    $.fn.editable.defaults.mode = 'inline';

    $('#priority').editable({
        type: 'select',
        title: 'Priority',
        placement: 'right',
        value: 2,
	source: globalDataSources['priority'],
    });

    $('#tasklist').editable({
        type: 'select',
        title: 'Task list',
        placement: 'right',
        value: 1,
	source: globalDataSources['tasklist'],
    });

    $("#title").editable({
        type: 'text',
        title: 'Title',
        clear: true,
        placeholder: 'task title',
    });

// description is now an independent textarea
// not using editable because it doesn't look nice

    $("#responsible").editable({
        type: 'select',
        value: 1,
        title: 'Responsible',
        placement: 'right',
	source: globalDataSources['responsible'],
    });

};

$(document).ready(function () {

    // Setup - add a text input to each footer cell
    // but they become header cells due to the CSS added in index.html
    //   <tfoot style="display: table-header-group;">
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

	globalDataSources = dataSources;
	initializeEditables();
    } );
    
});
