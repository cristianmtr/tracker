# TODO

- in order to accomodate for multiple users modifying and creating tasks in the database, I should do the following:
  - create a queue with submitData objects;
  - have a process pop from the queue and do the task;
  - after each task is processed, the client browser should be informed what row_id it needs to update;

## PROBLEMATIC
- caching dictionary of user ids to user names (and others) will need to be refreshed when there's a change;
  - poss. solution: if a submitData req. affects any of these, the row_id to be updated will be a reserved code (e.g. -1);
  - stress the client, not the server;

## NOTES

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
  
### DEPLOYMENT

- I am using an existing database based on [taskfreak](http://www.taskfreak.com/);
- username and password are provided in a config.json file;
- Example of config.json:
```javascript
{
    'username' : 'youruser',
    'password' : 'yourpass'
}
```
