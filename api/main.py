from typing import Any, Dict, List

# Simple starter project to test installation and environment.
# Based on https://fastapi.tiangolo.com/tutorial/first-steps/
from fastapi import FastAPI, Response, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
# Explicitly included uvicorn to enable starting within main program.
# Starting within main program is a simple way to enable running
# the code within the PyCharm debugger
import uvicorn

from db import DB

# Type definitions
KV = Dict[str, Any]  # Key-value pairs

app = FastAPI()

# NOTE: In a prod environment, never put this information in code!
# There are design patterns for passing confidential information to
# application.
# TODO: You may need to change the password
db = DB(
	host="localhost",
	port=3306,
	user="root",
	password="FuckOffParis6969!!",
	database="s24_hw2",
)

@app.get("/")
async def healthcheck():
	return HTMLResponse(content="<h1>Heartbeat</h1>", status_code=status.HTTP_200_OK)


# TODO: all methods below

# --- STUDENTS ---

# HELPER FUNCTIONS
def return_fields(req: Request) -> List[str]:
	full_url = str(req.url)
	if 'fields=' in full_url:
		sub_str = full_url[full_url.find('fields=') + len('fields='):]
		fields = sub_str.split(',')
	else:
		fields = []
	return fields


@app.get("/students")
async def get_students(req: Request):
	"""Gets all students that satisfy the specified query parameters.

	For instance,
		GET http://0.0.0.0:8002/students
	should return all attributes for all students.

	For instance,
		GET http://0.0.0.0:8002/students?first_name=John&last_name=Doe
	should return all attributes for students whose first name is John and last name is Doe.

	You must implement a special query parameter, `fields`. You can assume
	`fields` is a comma-separated list of attribute names. For instance,
		GET http://0.0.0.0:8002/students?first_name=John&fields=first_name,email
	should return the first name and email for students whose first name is John.
	Not every request will have a `fields` parameter.

	You can assume the query parameters are valid attribute names in the student table
	(except `fields`).

	:param req: The request that optionally contains query parameters
	:returns: A list of dicts representing students. The HTTP status should be set to 200 OK.
	"""

	# Use `dict(req.query_params)` to access query parameters
	fields = return_fields(req)
	filters = dict(req.query_params) # after the '?' mark i.e. query_params {}
	filters.pop('fields', None)
	data = db.select('student', fields, filters)
	print('yo')
	return JSONResponse(content=data, status_code=200)


	# Need to def build_select_query(table: str, rows: List[str], filters: KV) -> Query:

@app.get("/students/{student_id}")
async def get_student(student_id: int, req: Request):
	"""Gets a student by ID.

	For instance,
		GET http://0.0.0.0:8002/students/1
	should return the student with student ID 1. The returned value should
	be a dict-like object, not a list.

	If the student ID doesn't exist, the HTTP status should be set to 404 Not Found.

	:param student_id: The ID to be matched
	:returns: If the student ID exists, a dict representing the student with HTTP status set to 200 OK.
				If the student ID doesn't exist, the HTTP status should be set to 404 Not Found.
	"""
	fields = return_fields(req)
	filters = {'student_id':int(student_id)} # after the '?' mark i.e. query_params {}
	data = db.select('student', fields, filters)

	if len(data) == 0:
		return HTMLResponse(content=None, status_code=404)
	else:
		data=data[0]
		return JSONResponse(content=data, status_code=200)



@app.post("/students")
async def post_student(req: Request):
	"""Creates a student.

	You can assume the body of the POST request is a JSON object that represents a student.
	You can assume the request body contains only attributes found in the student table and does not
	attempt to set `student_id`.

	For instance,
		POST http://0.0.0.0:8002/students
		{
			"first_name": "John",
			"last_name": "Doe",
			...
		}
	should create a student with the attributes specified in the request body.

	If the email is not specified in the request body, the HTTP status should be set to 400 Bad Request.
	If the email already exists in the student table, the HTTP status should be set to 400 Bad Request.
	If the enrollment year is not valid, the HTTP status should be set to 400 Bad Request.

	:param req: The request, which contains a student JSON in its body
	:returns: If the request is valid, the HTTP status should be set to 201 Created.
				If the request is not valid, the HTTP status should be set to 400 Bad Request.
	"""

	# Use `await req.json()` to access the request body
	req_data = await req.json()

	if 'email' not in req_data.keys():
		return HTMLResponse(content=None,status_code=400)

	email_data = db.select('student',['email'], {})
	emails = [d['email'] for d in email_data]

	if req_data['email'] in emails:
		return HTMLResponse(content=None, status_code=400)

	enroll_req_data = req_data['enrollment_year']
	try:
		enroll_year = int(enroll_req_data)
	except ValueError:
		return HTMLResponse(content=None, status_code=400)

	enroll_year = int(enroll_year)
	print(enroll_year)
	if enroll_year < 2016 or enroll_year > 2024:
		return HTMLResponse(content=None, status_code=400)

	insert = db.insert('student', req_data)
	if insert==0:
		return HTMLResponse(content=None, status_code=400)

	return HTMLResponse(content=None, status_code=201)



@app.put("/students/{student_id}")
async def put_student(student_id: int, req: Request):
	"""Updates a student.

	You can assume the body of the PUT request is a JSON object that represents a student.
	You can assume the request body contains only attributes found in the student table and does not
	attempt to update `student_id`.

	For instance,
		PUT http://0.0.0.0:8002/students/1
		{
			"first_name": "Joe"
		}
	should update the student with student ID 1's first name to Joe.

	If the student does not exist, the HTTP status should be set to 404 Not Found.
	If the email is set to null in the request body, the HTTP status should be set to 400 Bad Request.
	If the email already exists in the student table, the HTTP status should be set to 400 Bad Request.
	If the enrollment year is not valid, the HTTP status should be set to 400 Bad Request.

	:param student_id: The ID of the student to be updated
	:param req: The request, which contains a student JSON in its body
	:returns: If the request is valid, the HTTP status should be set to 200 OK.
				If the request is not valid, the HTTP status should be set to the appropriate error code.
	"""

	# Use `await req.json()` to access the request body
	req_data = await req.json()

	id_data = db.select('student', ['student_id'], {})
	ids = [d['student_id'] for d in id_data]
	if student_id not in ids:
		return HTMLResponse(content=None, status_code=404)

	# Python automatically changes null in json to None
	if req_data.get('email','Key not found') is None:
		return HTMLResponse(content=None, status_code=400)

	email_data = db.select('student', ['email'], {})
	emails = [d['email'] for d in email_data]
	if req_data.get('email', 0) in emails:
		return HTMLResponse(content=None, status_code=400)

	enroll_req_data = req_data['enrollment_year']
	try:
		enroll_year = int(enroll_req_data)
	except ValueError:
		return HTMLResponse(content=None, status_code=400)

	enroll_year = int(enroll_year)
	print(enroll_year)
	if enroll_year < 2016 or enroll_year > 2024:
		return HTMLResponse(content=None, status_code=400)

	update = db.update('student', req_data, {'student_id': student_id})
	if update == 0:
		return HTMLResponse(content=None, status_code=400)

	return HTMLResponse(content=None, status_code=200)

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
	"""Deletes a student.

	For instance,
		DELETE http://0.0.0.0:8002/students/1
	should delete the student with student ID 1.

	If the student does not exist, the HTTP status should be set to 404 Not Found.

	:param student_id: The ID of the student to be deleted
	:returns: If the request is valid, the HTTP status should be set to 200 OK.
				If the request is not valid, the HTTP status should be set to 404 Not Found.
	"""
	id_data = db.select('student', ['student_id'], {})
	ids = [d['student_id'] for d in id_data]
	if student_id not in ids:
		return HTMLResponse(content=None, status_code=404)

	delete_res = db.delete('student',{'student_id': student_id})

	if delete_res == 0:
		return HTMLResponse(content=None, status_code=404)

	return HTMLResponse(content=None, status_code=200)



# --- EMPLOYEES ---

@app.get("/employees")
async def get_employees(req: Request):
	"""Gets all employees that satisfy the specified query parameters.

	For instance,
		GET http://0.0.0.0:8002/employees
	should return all attributes for all employees.

	For instance,
		GET http://0.0.0.0:8002/employees?first_name=Don&last_name=Ferguson
	should return all attributes for employees whose first name is Don and last name is Ferguson.

	You must implement a special query parameter, `fields`. You can assume
	`fields` is a comma-separated list of attribute names. For instance,
		GET http://0.0.0.0:8002/employees?first_name=Don&fields=first_name,email
	should return the first name and email for employees whose first name is Don.
	Not every request will have a `fields` parameter.

	You can assume the query parameters are valid attribute names in the employee table
	(except `fields`).

	:param req: The request that optionally contains query parameters
	:returns: A list of dicts representing employees. The HTTP status should be set to 200 OK.
	"""

	# Use `dict(req.query_params)` to access query parameters
	fields = return_fields(req)
	filters = dict(req.query_params)  # after the '?' mark i.e. query_params {}
	filters.pop('fields', None)
	data = db.select('employee', fields, filters)
	print('yo')
	return JSONResponse(content=data, status_code=200)




@app.get("/employees/{employee_id}")
async def get_employee(employee_id: int, req: Request):
	"""Gets an employee by ID.

	For instance,
		GET http://0.0.0.0:8002/employees/1
	should return the employee with employee ID 1. The returned value should
	be a dict-like object, not a list.

	If the employee ID doesn't exist, the HTTP status should be set to 404 Not Found.

	:param employee_id: The ID to be matched
	:returns: If the employee ID exists, a dict representing the employee with HTTP status set to 200 OK.
				If the employee ID doesn't exist, the HTTP status should be set to 404 Not Found.
	"""
	fields = return_fields(req)
	filters = {'employee_id': int(employee_id)}  # after the '?' mark i.e. query_params {}
	data = db.select('employee', fields, filters)

	if len(data) == 0:
		return HTMLResponse(content=None, status_code=404)
	else:
		data = data[0]
		return JSONResponse(content=data, status_code=200)





@app.post("/employees")
async def post_employee(req: Request):
	"""Creates an employee.

	You can assume the body of the POST request is a JSON object that represents an employee.
	You can assume the request body contains only attributes found in the employee table and does not
	attempt to set `employee_id`.

	For instance,
		POST http://0.0.0.0:8002/employees
		{
			"first_name": "Don",
			"last_name": "Ferguson",
			...
		}
	should create an employee with the attributes specified in the request body.

	If the email is not specified in the request body, the HTTP status should be set to 400 Bad Request.
	If the email already exists in the employee table, the HTTP status should be set to 400 Bad Request.
	If the employee type is not valid, the HTTP status should be set to 400 Bad Request.

	:param req: The request, which contains an employee JSON in its body
	:returns: If the request is valid, the HTTP status should be set to 201 Created.
				If the request is not valid, the HTTP status should be set to 400 Bad Request.
	"""

	# Use `await req.json()` to access the request body
	req_data = await req.json()

	if 'email' not in req_data.keys():
		return HTMLResponse(content=None, status_code=400)

	email_data = db.select('employee', ['email'], {})
	emails = [d['email'] for d in email_data]

	if req_data['email'] in emails:
		return HTMLResponse(content=None, status_code=400)

	et = req_data['employee_type']

	if et not in ['Professor','Lecturer','Staff']:
		return HTMLResponse(content=None, status_code=400)

	insert = db.insert('employee', req_data)
	if insert == 0:
		return HTMLResponse(content=None, status_code=400)

	return HTMLResponse(content=None, status_code=201)

@app.put("/employees/{employee_id}")
async def put_employee(employee_id: int, req: Request):
	"""Updates an employee.

	You can assume the body of the PUT request is a JSON object that represents an employee.
	You can assume the request body contains only attributes found in the employee table and does not
	attempt to update `employee_id`.

	For instance,
		PUT http://0.0.0.0:8002/employees/1
		{
			"first_name": "Donald"
		}
	should update the employee with employee ID 1's first name to Donald.

	If the employee does not exist, the HTTP status should be set to 404 Not Found.
	If the email is set to null in the request body, the HTTP status should be set to 400 Bad Request.
	If the email already exists in the employee table, the HTTP status should be set to 400 Bad Request.
	If the employee type is not valid, the HTTP status should be set to 400 Bad Request.

	:param employee_id: The ID of the employee to be updated
	:param req: The request, which contains an employee JSON in its body
	:returns: If the request is valid, the HTTP status should be set to 200 OK.
				If the request is not valid, the HTTP status should be set to the appropriate error code.
	"""

	# Use `await req.json()` to access the request body
	req_data = await req.json()

	# If the employee does not exist, the HTTP status should be set to 404 Not Found.
	id_data = db.select('employee', ['employee_id'], {})
	ids = [d['employee_id'] for d in id_data]
	if employee_id not in ids:
		return HTMLResponse(content=None, status_code=404)

	# If the email is set to null in the request body, the HTTP status should be set to 400 Bad Request.
	if req_data.get('email', 'Key not found') is None:
		return HTMLResponse(content=None, status_code=400)

	# If the email already exists in the employee table, the HTTP status should be set to 400 Bad Request.
	email_data = db.select('employee', ['email'], {})
	emails = [d['email'] for d in email_data]
	if req_data.get('email', 0) in emails:
		return HTMLResponse(content=None, status_code=400)

	# If the employee type is not valid, the HTTP status should be set to 400 Bad Request.
	if 'employee_type' in req_data.keys():
		et = req_data['employee_type']
		if et not in ['Staff', 'Professor', 'Lecturer']:
			return HTMLResponse(content=None, status_code=400)


	update = db.update('employee', req_data, {'employee_id': employee_id})
	if update == 0:
		return HTMLResponse(content=None, status_code=400)

	return HTMLResponse(content=None, status_code=200)




@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int):
	"""Deletes an employee.

	For instance,
		DELETE http://0.0.0.0:8002/employees/1
	should delete the employee with employee ID 1.

	If the employee does not exist, the HTTP status should be set to 404 Not Found.

	:param employee_id: The ID of the employee to be deleted
	:returns: If the request is valid, the HTTP status should be set to 200 OK.
				If the request is not valid, the HTTP status should be set to 404 Not Found.
	"""
	id_data = db.select('employee', ['employee_id'], {})
	ids = [d['employee_id'] for d in id_data]
	if employee_id not in ids:
		return HTMLResponse(content=None, status_code=404)

	delete_res = db.delete('employee', {'employee_id': employee_id})

	if delete_res == 0:
		return HTMLResponse(content=None, status_code=404)

	return HTMLResponse(content=None, status_code=200)



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8003)
