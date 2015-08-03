// TODO
var table;

// this will be used for submitting POST data to server
// should be -1 if the item submitted is new (doesn't exist in db)
// should be a specific id for an existing item if it's an UPDATE
var currentItemId = -1;

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

function prepareModalForNewTask() {
    currentItemId = -1;
    setDataInModal(newItemForModal);
};

function submitTaskFromModal() {
    var dataToSubmit = JSON.stringify(
	{
	    'id': currentItemId,
	    'priority' : $('#priority').editable('getValue')['priority'],
	    'deadline' : $('#deadline').data("DateTimePicker").date().format("YYYY-MM-DD"),
	    'tasklist' : $('#tasklist').editable('getValue')['tasklist'],
	    'title' : $('#title').editable('getValue')['title'],
	    'description' : $('#description').val(),
	    'responsible' : $('#responsible').editable('getValue')['responsible'],
	}
    )
    $.ajax({
	url:'/post',
	type:'POST',
	data:dataToSubmit,
	contentType:"application/json; charset=utf-8",
	success: submitTaskSuccessCallback,
    });
};

function replaceIdsWithValues(dataSet) {
    // we replace the ID numbers we get from the server
    // with the names from the dictionary mapping we will store client-side
    for (var i = 0; i < dataSet.length; i++) {
	var responsible_id = dataSet[i]['responsible'];
	var author_id = dataSet[i]['author'];
	if (responsible_id != null) {
	    dataSet[i]['responsible'] = dataSources['responsible'][responsible_id];
	};
	if (author_id != null) {
	    dataSet[i]['author'] = dataSources['responsible'][author_id];
	};
    };
    return dataSet;

};

function idExistsInTableRows(idToCheck) {
    if (table.row("#" + idToCheck).data() == undefined )
    {
	return false;
    }
    return true;
};

function addNewRowAndRedrawTable(newTaskId, jsonDataObject) {
    table.row.add({
	"title":jsonDataObject['title'],
	"description":jsonDataObject['description'],
	"deadline" : jsonDataObject["deadline"],
	"responsible" : jsonDataObject["responsible"],
	"author" : jsonDataObject["author"],
	"DT_RowId" : newTaskId,
    });
};

function submitTaskSuccessCallback(response) {
    console.log(response);
    var idToUpdate = response['data'];
    if (idToUpdate == -1)
    {
	alert ("There was a problem processing your request. Try again later");
	return;
    }
    $.ajax({
	url: '/json/'+idToUpdate,
	async: true,
	dataType: 'json',
	success: function(jsonDataObject) {
	    jsonDataObject = jsonDataObject['data'];
	    jsonDataObject = replaceIdsWithValues([jsonDataObject])[0];
	    if ( idExistsInTableRows(idToUpdate) )
	    {
		setDataInRowById(idToUpdate, jsonDataObject);
	    }
	    else {
		addNewRow(idToUpdate, jsonDataObject);
	    }
	    table.draw();
	}
    });
};

function setDataInRowById(DT_RowId, dataObject) {
    console.log("trying to update row " + DT_RowId + " with data " + dataObject);
    table.row("#"+DT_RowId).data(dataObject);
};

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

function updateDataInModalFromId() {
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

function toggleModal() {
    $("#createNewModal").modal('toggle');
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
	dataSources = data['dataSources'];
        dataSet = data['data'];
	dataSet = replaceIdsWithValues(dataSet);
	table = $('#example').DataTable({
            "data": dataSet,
            "columns": [
		{"data":"title"},
		{"data":"description"},
		{"data":"deadline"},
		{"data":"responsible"},
		{"data":"author"}
	    ]
        });

	//on click functionality
	$('#example tbody').on('click', 'tr', function () {
            currentItemId = this.id;
	    console.log('clicked on row with id ', currentItemId);
	    updateDataInModalFromId();
	    toggleModal();
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
