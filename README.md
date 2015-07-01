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
  
### DEPLOYMENT

- I am using an existing database based on [taskfreak](http://www.taskfreak.com/);
- username and password are provided in a config.json file;
Example of config.json:
```javascript
{
    'username' : 'youruser',
    'password' : 'yourpass'
}
```
