````markdown
# CodeCraftHub REST API

## Project Overview

CodeCraftHub is a beginner-friendly REST API built with **Python** and **Flask** for managing online learning courses. The application demonstrates the fundamental CRUD (Create, Read, Update, Delete) operations using a JSON file as the data store instead of a database.

This project is ideal for students learning:

- REST API development
- HTTP methods
- Flask web framework
- JSON data handling
- API testing
- CRUD operations

---

# Features

- Create new courses
- View all courses
- View a single course by ID
- Update existing courses
- Delete courses
- JSON file storage (no database required)
- Input validation
- Proper HTTP status codes
- Error handling
- Beginner-friendly code structure

---

# Technologies Used

- Python 3
- Flask
- JSON
- REST API
- Requests (for testing)
- unittest

---

# Project Structure

```
CodeCraftHub/
│
├── app.py
├── test_api.py
├── requirements.txt
├── README.md
│
└── data/
    └── courses.json
```

### File Description

| File | Purpose |
|-------|----------|
| app.py | Main Flask application |
| test_api.py | Automated API tests |
| requirements.txt | Python dependencies |
| README.md | Project documentation |
| data/courses.json | Stores course data |

---

# Installation

## Step 1: Install Python

Download Python from:

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

or

```bash
python3 --version
```

---

## Step 2: Clone or Download the Project

If using Git:

```bash
git clone https://github.com/yourusername/CodeCraftHub.git
```

Or simply download the project folder.

---

## Step 3: Open the Project Folder

```bash
cd CodeCraftHub
```

---

## Step 4: Create a Virtual Environment (Recommended)

Windows

```bash
python -m venv venv
```

Mac/Linux

```bash
python3 -m venv venv
```

Activate it.

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

---

## Step 5: Install Dependencies

```bash
pip install flask requests
```

Or if using requirements.txt

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the Flask server.

```bash
python app.py
```

You should see something similar to:

```
* Running on http://127.0.0.1:5001
```

The API is now available at

```
http://127.0.0.1:5001
```

---

# API Endpoints

## 1. Home

### GET /

Returns a welcome message.

Example:

```bash
curl http://127.0.0.1:5001/
```

Response

```json
{
  "message": "CodeCraftHub API up. Use /api/courses endpoints."
}
```

---

## 2. Get All Courses

### GET /api/courses

Example

```bash
curl http://127.0.0.1:5001/api/courses
```

Response

```json
[]
```

or

```json
[
  {
    "id": 1,
    "name": "Python",
    "description": "Learn Python",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-08-03T18:30:00Z"
  }
]
```

---

## 3. Create a Course

### POST /api/courses

Example

```bash
curl -X POST http://127.0.0.1:5001/api/courses \
-H "Content-Type: application/json" \
-d '{
"name":"Python Fundamentals",
"description":"Learn Python",
"target_date":"2026-12-31",
"status":"Not Started"
}'
```

Response

```json
{
  "id": 1,
  "name": "Python Fundamentals",
  "description": "Learn Python",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-08-03T18:30:00Z"
}
```

---

## 4. Get One Course

### GET /api/courses/1

Example

```bash
curl http://127.0.0.1:5001/api/courses/1
```

---

## 5. Update a Course

### PUT /api/courses/1

Example

```bash
curl -X PUT http://127.0.0.1:5001/api/courses/1 \
-H "Content-Type: application/json" \
-d '{
"name":"Advanced Python",
"description":"Master Python",
"target_date":"2027-01-01",
"status":"In Progress"
}'
```

---

## 6. Delete a Course

### DELETE /api/courses/1

Example

```bash
curl -X DELETE http://127.0.0.1:5001/api/courses/1
```

Response

```json
{
  "message": "Deleted",
  "id": 1
}
```

---

# Course JSON Format

```json
{
  "id": 1,
  "name": "Python Fundamentals",
  "description": "Learn Python programming",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-08-03T18:30:00Z"
}
```

---

# Valid Status Values

The API only accepts the following status values:

- Not Started
- In Progress
- Completed

---

# HTTP Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Bad Request |
| 404 | Course Not Found |
| 500 | Internal Server Error |

---

# Running the Tests

Start the API first.

```bash
python app.py
```

Open another terminal and run:

```bash
python test_api.py
```

Expected output:

```
Ran 17 tests in 0.20s

OK
```

---

# Example Error Responses

Missing field

```json
{
  "error": "Missing field: target_date"
}
```

Invalid status

```json
{
  "error": "status must be one of ['Completed', 'In Progress', 'Not Started']"
}
```

Invalid date

```json
{
  "error": "target_date must be YYYY-MM-DD"
}
```

Course not found

```json
{
  "error": "Course not found"
}
```

---

# Troubleshooting

## ModuleNotFoundError

Install the required packages.

```bash
pip install flask requests
```

---

## Address already in use

Another program is using port 5001.

Stop the existing program or change the port inside `app.py`.

Example:

```python
app.run(port=5002)
```

---

## 404 Not Found

Check that:

- The Flask server is running.
- The URL is correct.
- The course ID exists.

---

## JSON Decode Error

Make sure requests include:

```http
Content-Type: application/json
```

and that your JSON is valid.

---

## Tests Fail

Verify:

- The server is running.
- BASE_URL in `test_api.py` is correct.
- Flask is listening on port 5001.

---

# Learning Outcomes

After completing this project, you should understand:

- What REST APIs are
- CRUD operations
- HTTP request methods
- JSON request and response formats
- Flask routing
- Input validation
- Error handling
- Automated API testing with unittest

---

# Future Improvements

Possible enhancements include:

- SQLite or MySQL database support
- User authentication
- Course categories
- Search functionality
- Pagination
- PATCH endpoint
- Swagger/OpenAPI documentation
- Docker support
- JWT authentication
- Web frontend

---

# Author

CodeCraftHub REST API

A beginner-friendly Flask project for learning REST API development.
````
