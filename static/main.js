var dataSet;

$(document).ready(function() {
    $.fn.editable.defaults.mode = 'inline';         

    $(function() {
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
    });
    
    function test() {
	return $.getJSON('/json');
    }

    $.when(test()).then(function(data) {
	dataSet = data['data'];
	$('#example').DataTable({
	    "data" : dataSet,
	    "columns" : [ {
		"title" : "id"
	    }, {
		"title" : "description"
	    }, {
		"title" : "dead line"
	    }, {
		"title" : "responsible"
	    }, {
		"title" : "author"
	    } ]
	});
    });
});
