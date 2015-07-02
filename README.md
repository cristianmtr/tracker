# TODO

- [x] jsonify database
- [ ] create in place
  - [ ] ajax call to last created
- [ ] edit in place
  - [ ] ajax call for that one

- Check here for create in place js: http://vitalets.github.io/x-editable/docs.html#newrecord

- consider how you want to handle the server's response to a /post request
  - x-editable provides a success callback;
- when sending /post request, you can access value from fields using x-editable again:
  - e.g. $("#tasklist").editable('getValue');
  - for datepicker, $('#deadline').data("DateTimePicker").date().format("DD/MMMM/YYYY");

- use template from before;
  - make it a table
- make function to insert data into the cells;
```python
for entry in listObject:
	insertIntoCell(tableRow[currindex], listObject[currIndex])
```
  - take data from example table cells;

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
