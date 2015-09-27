# TRACKER

A simple task tracker. With REST API, token authentication, and a nice [datatables](http://datatables.net/)-based UI

Work in progress

# TODO

## FIX

- add <id-type column>_text to json endpoints;
- support proper encoding of national chars;
- don't depend on mappings between client-side attributes and database ones (see: feature - move to SQLA);
- don't submit data if it has been changed in the meanwhile;

## FEATURE

- move to SQLAlchemy for schema;

- in order to accommodate for multiple users modifying and creating tasks in the database, I should do the following:
  - have a dict mapping user_token to last time the user got an update;
  - have another dict mapping time of entry update/creation to type of item and its unique id;
  - periodically, js client will send a request and get back a list of all the items it has to update;
  - will have a counter displayed for the user;
  - on click, go through the list, asking for the data;
    - each piece, update the table or its in-memory store of user_ids, tasklists etc.;
	- for the editing the user has done, we will maintain another list of objects ({"id":<id>,"type":<type>}) and at the time of going through the notifications list, we will NOT get these;
  - when clicking SUBMIT, check if the data has been changed in the db before possibly overwriting it;
    - have a timestamp on each entry, 'lastmodified', with date_time;
    - check if greater than the timestamp the user has in memory on the client side;
    - don't drop the changes he/she made in the form;
      - offer dialogue option: overwrite, reload and drop, store;
        - store: keep what the user has written in memory;
	- show in the form what is now in the database;
	- dialogue in the form (that is normally hidden) : keep this or overwrite;

- to handle token authorization
    - client sends username and password to /auth;
    - server generates token (with TTL) and returns it to client;
        - is stored in memory;
    - client js stores it as cookie (?);
    - is used as parameter for every request;
    
- caching dictionary of user ids to user names (and others) will need to be refreshed when there's a change;
  - poss. solution: if a submitData req. affects any of these, the row_id to be updated will be a reserved code (e.g. -1);
  - stress the client, not the server;

## NOTES
- on page load, check if session['username'] is set, and update html accordingly;

- in frk_memberProject you have mappings informing about each user's position within each of the projects;
    - as far as I can tell, it's 0 - request, 
    1 - member (can post tasks, can post comments, can modify tasks)
    ...
    4 - moderator (can delete tasks)
    5 - admin (can delete the list itself)

- in order to access data from a specific row:
```javascript
table.row("#93").data();
```
- [x] jsonify database
- [ ] create in place
  - [ ] ajax call to last created
- [ ] edit in place
  - [ ] ajax call for that one

- consider how you want to handle the server's response to a /post request
  - x-editable provides a success callback;
- when sending /post request, you can access value from fields using x-editable again:
  - e.g. $("#tasklist").editable('getValue');
  - for datepicker, $('#deadline').data("DateTimePicker").date().format("YYYY-MM-DD");
- for modifying the data in the modal when click on an existing task:
  -  $('#responsible').editable('setValue',1);
  - the nr corresponds to the index of the item;
  - e.g.: 1 -> 'Urgent'
```javascript
          source: [
            {value: 1, text: 'Urgent'},
            {value: 2, text: 'Medium'},
            {value: 3, text: 'Low'}
        ]
```

- when calling Create New: execute make fields in modal editable with defaults as per new task;
    - otoh, when calling Edit Task (todo), call the function in js to fill the fields in the modal with the values from the task;
- options for selects should be provided by the server on the initial call and stored in some client-side variable; 
  
### INSTALL

- I am using an existing database based on [taskfreak](http://www.taskfreak.com/);
- username and password are provided in a config.json file;
- Example of config.json:
```javascript
{
    'username' : 'youruser',
    'password' : 'yourpass'
}
```
