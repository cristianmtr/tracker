var table;

// this will be used for submitting POST data to server
// should be -1 if the item submitted is new (doesn't exist in db)
// should be a specific id for an existing item if it's an UPDATE
var currentItemId = -1;

const newItemForModal = {
    'title': '',
    'deadline': new moment().format("YYYY-MM-DD"),
    'priority': 2,
    'responsible': '',
    'description': '',
    'author': '',
    'tasklist': 2,
}

var globalDataSources;

function setUItoLoggedOut() {
    docCookies.removeItem("username");
    docCookies.removeItem("token");
    $("#userstatus").text("Not logged in");
    $("#authHolder").show();
    $("#userInfo").hide();
    $("#loginButton").show();
    $("#logoutButton").hide();
    $("#username").val("");
    $("#password").val("");
}

function logoutSuccessCallback(response) {
    if (response['code'] == 200) {
        setUItoLoggedOut();
    }
    else {
        console.log("there was a problem in logoutSuccessCallback")
    }
}

function logOut() {
    // send POST to /auth
    // auth deletes session
    // returns success
    var dataToSubmit = JSON.stringify(
        {
            "username": docCookies.getItem("username"),
            "token": docCookies.getItem("token"),
        }
    );
    $.ajax({
        url: '/logout',
        type: 'POST',
        data: dataToSubmit,
        contentType: "application/json; charset=utf-8",
        success: logoutSuccessCallback,
    });
};

function prepareModalForNewTask() {
    currentItemId = -1;
    setDataInModal(newItemForModal);
    $("#content").hide();
};

function setUItoLoggedIn() {
    username = docCookies.getItem("username");
    $("#userstatus").text(username);
    $("#authHolder").hide();
    $("#loggedInAs").text("Logged in as " + username);
    $("#userInfo").show();
    $("#loginButton").hide();
    $("#logoutButton").show();
}

function authenticationResponseHandler(response) {
    console.log(JSON.stringify(response));
    console.log(response);
    if (response['code'] == 200) {
        $("#authModal").modal("hide");
        // as per server, it's 14 days
        var expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate()+14);
        //TODO change last parameter (https only) to true
        docCookies.setItem("token",response['data']['token'], expirationDate.toGMTString(),null,null,null);
        docCookies.setItem("username",response['data']['username']);
        setUItoLoggedIn();
    }
    else {
        // add some red text html to the modal
        // saying 'try again'
        $("#authmessage").text("Failure. Try again");
    }


};

function tryAuthenticate() {
    var username = $("#username").val();
    var password = $("#password").val();
    var dataToSubmit = JSON.stringify(
        {
            'username': username,
            'password': password,
        }
    );
    $("#authmessage").text("");
    $.ajax({
        url: '/auth',
        type: 'POST',
        data: dataToSubmit,
        contentType: "application/json; charset=utf-8",
        success: authenticationResponseHandler,
    });
}

function submitTaskFromModal() {
    var dataToSubmit = JSON.stringify(
        {
            'data': {
                'id': currentItemId,
                'priority': $('#priority').editable('getValue')['priority'],
                'deadline': $('#deadline').data("DateTimePicker").date().format("YYYY-MM-DD"),
                'tasklist': $('#tasklist').editable('getValue')['tasklist'],
                'title': $('#title').editable('getValue')['title'],
                'description': $('#description').val(),
                'responsible': $('#responsible').editable('getValue')['responsible'],
            },
            'auth': {
                'token': docCookies.getItem('token'),
            },
        }
    );
    $.ajax({
        url: '/post',
        type: 'POST',
        data: dataToSubmit,
        contentType: "application/json; charset=utf-8",
        success: submitTaskSuccessCallback,
    });
};

function replaceIdsWithValues(dataSet) {
    // we replace the ID numbers we get from the server
    // with the names from the dictionary mapping we will store client-side
    for (var i = 0; i < dataSet.length; i++) {
        var responsible_id = dataSet[i]['responsible'];
        var author_id = dataSet[i]['author'];
        var tasklist_id = dataSet[i]['tasklist'];
        var priority = dataSet[i]['priority'];
        if (responsible_id != null) {
            dataSet[i]['responsible'] = dataSources['responsible'][responsible_id];
        }
        ;
        if (author_id != null) {
            dataSet[i]['author'] = dataSources['responsible'][author_id];
        }
        ;
        if (tasklist_id != null) {
            dataSet[i]['tasklist'] = dataSources['tasklist'][tasklist_id];
        }
        ;
        if (priority != null) {
            dataSet[i]['priority'] = dataSources['priority'][priority];
        }
        ;
    }
    ;
    return dataSet;

};

function idExistsInTableRows(idToCheck) {
    if (table.row("#" + idToCheck).data() == undefined) {
        return false;
    }
    return true;
};

function addNewRow(newTaskId, jsonDataObject) {
    table.row.add({
        "title": jsonDataObject['title'],
        "description": jsonDataObject['description'],
        "tasklist": jsonDataObject["tasklist"],
        "priority": jsonDataObject["priority"],
        "deadline": jsonDataObject["deadline"],
        "responsible": jsonDataObject["responsible"],
        "author": jsonDataObject["author"],
        "DT_RowId": newTaskId,
    });
};

function submitTaskSuccessCallback(response) {
    console.log(response);
    if (response['code'] === 200) {
        var idToUpdate = response['data'];
        $.ajax({
            url: '/task/' + idToUpdate,
            async: true,
            dataType: 'json',
            success: function (jsonDataObject) {
                jsonDataObject = jsonDataObject['data'];
                jsonDataObject = replaceIdsWithValues([jsonDataObject])[0];
                if (idExistsInTableRows(idToUpdate)) {
                    setDataInRowById(idToUpdate, jsonDataObject);
                }
                else {
                    addNewRow(idToUpdate, jsonDataObject);
                }
                table.draw();
            }
        });
    }
    else {
        alert("Not logged in");
    }

};

function setDataInRowById(DT_RowId, dataObject) {
    console.log("trying to update row " + DT_RowId + " with data " + JSON.stringify(dataObject));
    table.row("#" + DT_RowId).data(dataObject);
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

function onClickTableRow(e) {
    currentItemId = e.id;
    console.log('clicked on row with id ', currentItemId);
    updateDataInModalFromId();
    toggleModal();
    $("#content").show();
};

function updateDataInModalFromId() {
    $.ajax({
        url: '/task/' + currentItemId,
        async: true,
        dataType: 'json',
        success: function (modalDataObject) {
            modalDataObject = modalDataObject['data'];
            console.log("got data from server: " + JSON.stringify(modalDataObject));
            setDataInModal(modalDataObject);
        }
    });
    $.ajax({
        url: '/comments/' + currentItemId,
        async: true,
        dataType: 'json',
        success: function (comments) {
            comments = comments['data'];
            console.log("got data from server: " + JSON.stringify(comments));
            fillCommentSection(comments);
        }
    });
    $.ajax({
        url: '/history/' + currentItemId,
        async: true,
        dataType: 'json',
        success: function (historyEntries) {
            historyEntries = historyEntries['data'];
            console.log("got data from server: " + JSON.stringify(historyEntries));
            fillHistorySection(historyEntries);
        }
    });
};

function toggleModal() {
    $("#createNewModal").modal('toggle');
};

function setDataInModal(modalDataObject) {
    $('#priority').editable('setValue', modalDataObject['priority']);
    $('#deadline').data("DateTimePicker").date(modalDataObject['deadline']);
    $('#tasklist').editable('setValue', modalDataObject['tasklist']);
    $('#title').editable('setValue', modalDataObject['title']);
    $('#description').val(modalDataObject['description']);
    $('#responsible').editable('setValue', modalDataObject['responsible']);

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

function fillCommentSection(comments) {
    var commentsContainer = $("#commentsList");
    commentsContainer.html("");
    for (var i in comments) {
        // TODO proper
        commentsContainer.prepend("<p>" + JSON.stringify(comments[i]) + "</p>");
    }
    ;
};

function fillHistorySection(historyEntries) {
    var historyContainer = $("#historyList");
    historyContainer.html("");
    for (var i = 0; i < historyEntries.length; i++) {
        historyContainer.prepend("<p>" + JSON.stringify(historyEntries[i]) + "</p>");
    }
    ;
};

function checkTokenAndUsernameCombinationCallback(response) {
    if (response['code'] === 200) {
        setUItoLoggedIn();
    }
    else {
        setUItoLoggedOut();
        alert("There was a problem with your credentials. Please try logging in again");
    }
}

function checkTokenAndUsernameCombination() {
    var dataToSubmit = JSON.stringify(
        {
            "username": docCookies.getItem("username"),
            "token": docCookies.getItem("token"),
        }
    );
    $.ajax({
        url: '/check',
        type: 'POST',
        data: dataToSubmit,
        contentType: "application/json; charset=utf-8",
        success: checkTokenAndUsernameCombinationCallback,
    });
}

function checkForTokenCookie() {
    if (docCookies.hasItem("token") === true && docCookies.hasItem("username") === true) {
        checkTokenAndUsernameCombination();
    }
    else {
        setUItoLoggedOut();
    }

}

$(document).ready(function () {

    // Setup - add a text input to each footer cell
    // but they become header cells due to the CSS added in index.html
    //   <tfoot style="display: table-header-group;">
    $('#example tfoot th').each(function () {
        var title = $('#example thead th').eq($(this).index()).text();
        $(this).html('<input style="width: 100%;" type="text" placeholder="search..." />');
    });

    function test() {
        return $.getJSON('/json');
    }

    // init bootstrap tab menu in modal
    $('#modaltabs').tab();

    $.when(test()).then(function (data) {
        console.log('got data from /json');
        dataSources = data['dataSources'];
        dataSet = data['data'];
        dataSet = replaceIdsWithValues(dataSet);
        table = $('#example').DataTable({
            "dom": 'C<"clear"><"toolbar">lfrtip',
            "data": dataSet,
            "columns": [
                {"data": "title"},
                {"data": "description"},
                {"data": "deadline"},
                {"data": "responsible"},
                {"data": "author"},
                {"data": "tasklist"},
                {"data": "priority"},
            ]
        });

        $("div.toolbar").html('<button id="userstatus" type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#authModal">Not logged in</button><div id="otherdiv"></div>');

        //on click functionality
        $('#example tbody').on('click', 'tr', function () {
            onClickTableRow(this);
        });

        // Apply the search
        table.columns().every(function () {
            var that = this;

            $('input', this.footer()).on('keyup ', function () {
                that
                    .search(this.value)
                    .draw();
            });
        });

        globalDataSources = dataSources;
        initializeEditables();
        checkForTokenCookie();
    });


});
