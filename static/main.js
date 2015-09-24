var table;

// this will be used for submitting POST data to server
// should be -1 if the item submitted is new (doesn't exist in db)
// should be a specific id for an existing item if it's an UPDATE
var currentItemId = -1;

const newItemForModal = {
    'title': '',
    'deadline': new moment().format("YYYY-MM-DD"),
    'priority': "Normal",
    'responsible': '',
    'description': '',
    'author': '',
    'tasklist': "General OPS",
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

function authenticationResponseHandler(response, username) {
    console.log(JSON.stringify(response));
    console.log(response);
    if (response['code'] == 200) {
        $("#authModal").modal("hide");
        // as per server, it's 14 days
        var expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + 14);
        //TODO change last parameter (https only) to true
        docCookies.setItem("token", response['data']['token'], expirationDate.toGMTString(), null, null, null);
        docCookies.setItem("username", username);
        setUItoLoggedIn();
    }
    else {
        // add some red text html to the modal
        // saying 'try again'
        $("#authmessage").text("Failure. Try again");
    }
}

function tryAuthenticate() {
    var username = $("#username").val();
    var password = $("#password").val();
    var dataToSubmit = JSON.stringify(
        {
            'username': username,
            'password': password
        }
    );
    $("#authmessage").text("");
    $.ajax({
        url: '/auth',
        type: 'POST',
        data: dataToSubmit,
        contentType: "application/json; charset=utf-8",
        success: function (response) {
            authenticationResponseHandler(response, username);
        }
    });
}

function alertModal(message) {
    $("#alertMessage").text(message);
    $("#alertModal").modal("toggle");
}

function submitTaskSuccessCallback(response, thisItemId, dataToSubmit) {
    console.log(response);


    if (response['code'] === 200) {
        if (thisItemId === -1) {
            // we have created a new task
            // we get the id assigned to the newly
            // created task from the response
            thisItemId = response['data'];
            addNewRow(thisItemId, dataToSubmit);
        }
        else {
            // we have updated an existing task
            setDataInRowById(thisItemId, dataToSubmit);
        }
        ;
    }
    else if (response['code'] === 401) {
        alertModal("Not logged in");
    }
    else {
        alertModal("Something went wrong. Please try again later");
    }
}

function submitTaskFromModal() {
    var thisItemId = currentItemId;
    var data = {
        'title': $("#title").val(),
        'priority': $('#priority').val(),
        'deadline': $('#deadline').data("DateTimePicker").date().format("YYYY-MM-DD"),
        'tasklist': $('#tasklist').val(),
        'description': $('#description').val(),
        'responsible': $('#responsible').val(),
        'author': $('#author').val(),
    };
    var dataToSubmit = JSON.stringify(
        {
            'data': data,
            'auth': {
                'token': docCookies.getItem('token'),
            },
        }
    );
    var url = "/task/";
    if (thisItemId !== -1) {
        url = "/task/" + thisItemId;
    }
    console.log("submit to " + url);
    $.ajax({
        url: url,
        type: 'POST',
        data: dataToSubmit,
        contentType: "application/json; charset=utf-8",
        success: function (response) {
            submitTaskSuccessCallback(response, thisItemId, data);
        }
    });
}

function replaceIdsWithValuesInDataSet(dataSet) {
    for (var i = 0; i < dataSet.length; i++) {
        dataSet[i] = replaceIdsWithValues(dataSet[i]);
    }
    return dataSet;
}

function replaceIdsWithValues(dataObject) {
    // we replace the ID numbers we get from the server
    // with the names from the dictionary mapping we will store client-side
    var responsible_id = dataObject['responsible'];
    var author_id = dataObject['author'];
    var tasklist_id = dataObject['tasklist'];
    var priority = dataObject['priority'];
    if (responsible_id != null) {
        dataObject['responsible'] = dataSources['responsible'][responsible_id];
    }
    ;
    if (author_id != null) {
        dataObject['author'] = dataSources['responsible'][author_id];
    }
    ;
    if (tasklist_id != null) {
        dataObject['tasklist'] = dataSources['tasklist'][tasklist_id];
    }
    ;
    if (priority != null) {
        dataObject['priority'] = dataSources['priority'][priority];
    }
    ;
    return dataObject;

};

function addValueFieldsToRowObject(dataObject) {
    var responsible_id = dataObject['responsible'];
    var author_id = dataObject['author'];
    var tasklist_id = dataObject['tasklist'];
    var priority = dataObject['priority'];
    if (responsible_id != null) {
        dataObject['responsible_text'] = dataSources['responsible'][responsible_id];
    }
    else {
        dataObject['responsible_text'] = "";
    }
    if (author_id != null) {
        dataObject['author_text'] = dataSources['responsible'][author_id];
    }
    else {
        dataObject['author_text'] = "";
    }
    if (tasklist_id != null) {
        dataObject['tasklist_text'] = dataSources['tasklist'][tasklist_id];
    }
    else {
        dataObject['tasklist_text'] = "";
    }
    if (priority != null) {
        dataObject['priority_text'] = dataSources['priority'][priority];
    }
    else {
        dataObject['priority_text'] = "";
    }
    return dataObject;
}

function idExistsInTableRows(idToCheck) {
    if (table.row("#" + idToCheck).data() == undefined) {
        return false;
    }
    return true;
};

function setAdditionalIDField(dataObject) {
    // WORKAROUND: dataTables does not read the ID field
    // to be displayed as column
    dataObject['ID'] = dataObject['DT_RowId'];
    return dataObject;
}

function addNewRow(newTaskId, jsonDataObject) {
    jsonDataObject = addValueFieldsToRowObject(jsonDataObject);
    jsonDataObject['DT_RowId'] = newTaskId;
    jsonDataObject = setAdditionalIDField(jsonDataObject);
    table.row.add(jsonDataObject);
    table.draw();
};

function setDataInRowById(DT_RowId, dataObject) {
    dataObject = addValueFieldsToRowObject(dataObject);
    dataObject['DT_RowId'] = DT_RowId;
    dataObject = setAdditionalIDField(dataObject);
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

function replaceValuesWithIds(modalDataObject) {
    var thisPriority = modalDataObject['priority'];
    var thisTasklist = modalDataObject['tasklist'];
    var thisResponsible = modalDataObject['responsible'];
    var thisAuthor = modalDataObject['author'];
    //for (var i=0;i<dataSources['priority'];i++) {
    //    if (dataSources['priority'][i] == thisPriority) {
    //        modalDataObject['priority'] = i;
    //    }
    //}
    //for (var i=0;i<dataSources['tasklist'];i++) {
    //    if (dataSources['tasklist'][i] == thisTasklist) {
    //        modalDataObject['tasklist'] = i;
    //    }
    //}
    //for (var i=0;i<dataSources['responsible'];i++) {
    //    if (dataSources['responsible'][i] == thisResponsible) {
    //        modalDataObject['responsible'] = i;
    //    }
    //    if (dataSources['responsible'][i] == thisAuthor) {
    //        modalDataObject['author'] = i;
    //    }
    //}
    for (var i in dataSources['priority']) {
        if (dataSources['priority'][i] === thisPriority) {
            modalDataObject['priority'] = i;
        }
    }
    for (var i in dataSources['tasklist']) {
        if (dataSources['tasklist'][i] === thisTasklist) {
            modalDataObject['tasklist'] = i;
        }
    }
    for (var i in dataSources['responsible']) {
        if (dataSources['responsible'][i] === thisResponsible) {
            modalDataObject['responsible'] = i;
        }
        if (dataSources['responsible'][i] === thisAuthor) {
            modalDataObject['author'] = i;
        }
    }
    return modalDataObject;
}

function updateDataInModalFromId() {
    var modalDataObject = table.row("#" + currentItemId).data();
    setDataInModal(modalDataObject);
    $.ajax({
        url: '/comments/' + currentItemId,
        async: true,
        dataType: 'json',
        success: function (comments) {
            comments = comments['data'];
            console.log("got comments from server: " + JSON.stringify(comments));
            fillCommentSection(comments);
        }
    });
    $.ajax({
        url: '/history/' + currentItemId,
        async: true,
        dataType: 'json',
        success: function (historyEntries) {
            historyEntries = historyEntries['data'];
            console.log("got history from server: " + JSON.stringify(historyEntries));
            fillHistorySection(historyEntries);
        }
    });
};

function toggleModal() {
    $("#createNewModal").modal('toggle');
};

function setDataInModal(modalDataObject) {
    $('#priority').val(modalDataObject["priority"]);
    $('#deadline').data("DateTimePicker").date(modalDataObject['deadline']);
    $("#tasklist").val(modalDataObject["tasklist"]);
    $("#title").val(modalDataObject["title"]);
    $('#description').val(modalDataObject['description']);
    $("#responsible").val(modalDataObject["responsible"]);
    console.log('data modal has been updated with ' + JSON.stringify(modalDataObject));
};

function getPriorityIDfromValue(priority) {
    for (var x in dataSources['priority']) {
        if (dataSources['priority'][x] === priority) {
            return x;
        }
    }
}

function getTasklistIDfromValue(tasklist) {
    for (var x in dataSources['tasklist']) {
        if (dataSources['tasklist'][x] === tasklist) {
            return x;
        }
    }
}

function getMemberIDfromValue(member) {
    for (var x in dataSources['responsible']) {
        if (dataSources['responsible'][x] === member) {
            return x;
        }
    }
}

function generateSelectOptionsForPriority() {
    var prioritySelect = $("#priority");
    prioritySelect.find("option").remove().end();
    for (var x in dataSources['priority']) {
        var opt = document.createElement('option');
        opt.value = x;
        opt.innerHTML = dataSources['priority'][x];
        prioritySelect.append(opt);
    }
}

function generateSelectOptionsForTasklist() {
    var tasklistSelect = $("#tasklist");
    tasklistSelect.find("option").remove().end();
    for (var x in dataSources['tasklist']) {
        var opt = document.createElement('option');
        opt.value = x;
        opt.innerHTML = dataSources['tasklist'][x];
        tasklistSelect.append(opt);
    }
}

function generateSelectOptionsForResponsible() {
    var responsibleSelect = $("#responsible");
    responsibleSelect.find("option").remove().end();
    for (var x in dataSources['responsible']) {
        var opt = document.createElement('option');
        opt.value = x;
        opt.innerHTML = dataSources['responsible'][x];
        responsibleSelect.append(opt);
    }
}

function initializeEditables() {

    generateSelectOptionsForPriority();

    generateSelectOptionsForTasklist();

    generateSelectOptionsForResponsible();
};

function fillCommentSection(comments) {
    var commentsContainer = $("#commentsList");
    commentsContainer.html("");
    for (var i in comments) {
        var cmdiv = '<div class="row task-modal-list-item">' + dataSources['responsible'][comments[i].author_id] + ", at " + comments[i].postDate + "</div>";
        cmdiv += "<div class='row'>" + comments[i].body + "</div>";
        commentsContainer.append(cmdiv);
        //(cmdiv);
    }
    ;
};

function fillHistorySection(historyEntries) {
    var historyContainer = $("#historyList");
    historyContainer.html("");
    for (var i in historyEntries) {
        var hsdiv = '<div class="row task-modal-list-item">';
        hsdiv += "Set to " + parseInt(historyEntries[i].statusKey) * 20 + "% by " + dataSources['responsible'][historyEntries[i].memberId] + " at " + historyEntries[i].statusDate;
        hsdiv += '</div>';
        historyContainer.append(hsdiv);
    }
    ;
};

function checkTokenAndUsernameCombinationCallback(response) {
    if (response['code'] === 200) {
        setUItoLoggedIn();
    }
    else {
        setUItoLoggedOut();
        alertModal("There was a problem with your credentials. Please try logging in again");
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

function loadRowsFromDataSet(dataSet) {
    for (var x in dataSet) {
        var row = dataSet[x];
        addNewRow(row['DT_RowId'], row);
    }
}

$(document).ready(function () {

    var opts = {
        lines: 13 // The number of lines to draw
        , length: 28 // The length of each line
        , width: 14 // The line thickness
        , radius: 42 // The radius of the inner circle
        , scale: 1 // Scales overall size of the spinner
        , corners: 1 // Corner roundness (0..1)
        , color: '#000' // #rgb or #rrggbb or array of colors
        , opacity: 0.25 // Opacity of the lines
        , rotate: 0 // The rotation offset
        , direction: 1 // 1: clockwise, -1: counterclockwise
        , speed: 1.5 // Rounds per second
        , trail: 100 // Afterglow percentage
        , fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
        , zIndex: 2e9 // The z-index (defaults to 2000000000)
        , className: 'spinner' // The CSS class to assign to the spinner
        , top: '50%' // Top position relative to parent
        , left: '50%' // Left position relative to parent
        , shadow: true // Whether to render a shadow
        , hwaccel: true // Whether to use hardware acceleration
        , position: 'absolute' // Element positioning
    }
    var target = document.getElementById('foo');
    var spinner = new Spinner(opts).spin(target);
    $("body").addClass("loading");

    // Setup - add a text input to each footer cell
    // but they become header cells due to the CSS added in index.html
    //   <tfoot style="display: table-header-group;">
    $('#example tfoot th').each(function () {
        var title = $('#example thead th').eq($(this).index()).text();
        $(this).html('<input style="width: 100%;" type="text" placeholder="search..." />');
    });

    function loadData() {
        return $.getJSON('/json');
    }

    //// init bootstrap tab menu in modal
    //$('#modaltabs').tab();

    $.when(loadData()).then(function (data) {
        console.log('got data from /json');
        dataSources = data['dataSources'];
        dataSet = data['data'];
        table = $('#example').DataTable({
            "dom": 'C<"clear"><"toolbar">lfrtip',
            scrollY: 800,
            scrollCollapse: true,
            fixedHeader: true,
            responsive: true,
            pagination: false,
            "columns": [
                {"data": "ID"},
                {"data": "title"},
                {"data": "description"},
                {"data": "deadline"},
                {"data": "responsible_text"},
                {"data": "author_text"},
                {"data": "tasklist_text"},
                {"data": "priority_text"}
            ],
            "order": [[3, "desc"]]
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


        loadRowsFromDataSet(dataSet);
        $("body").removeClass("loading");
    });


});
