from typing import Any, Dict, List

# Simple starter project to test installation and environment.
# Based on https://fastapi.tiangolo.com/tutorial/first-steps/
from fastapi import FastAPI, Response, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
# Explicitly included uvicorn to enable starting within main program.
# Starting within main program is a simple way to enable running
# the code within the PyCharm debugger
import uvicorn
import simplejson
from decimal import Decimal
from datetime import datetime


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
	database="fantasy_prod",
)


# HELPER FUNCTIONS
def convert_datetime_to_str(data):
    if isinstance(data, dict):
        return {key: convert_datetime_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_datetime_to_str(item) for item in data]
    elif isinstance(data, datetime):
        return data.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return data
	

def convert_decimal_to_float(data):
    if isinstance(data, dict):
        return {key: convert_decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_decimal_to_float(item) for item in data]
    elif isinstance(data, Decimal):
        return float(data)
    else:
        return data
	

def return_fields(req: Request) -> List[str]:
	full_url = str(req.url)
	if 'fields=' in full_url:
		sub_str = full_url[full_url.find('fields=') + len('fields='):]
		fields = sub_str.split(',')
	else:
		fields = []
	return fields
	


	




#ROUTES



@app.get("/")
async def healthcheck():
	return HTMLResponse(content="<h1>Heartbeat</h1>", status_code=status.HTTP_200_OK)





@app.get("/slateplayers/{slate_id}")
async def get_slateplayers(slate_id: int, req: Request):
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
	filters = {'slate_id':int(slate_id)} # after the '?' mark i.e. query_params {}
	data = db.select('slateplayer', fields, filters)

	if len(data) == 0:
		return HTMLResponse(content=None, status_code=404)
	else:
		data=convert_datetime_to_str(data)
		data=convert_decimal_to_float(data)
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






if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8003)
