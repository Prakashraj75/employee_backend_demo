# Employee Management Backend API

A beginner-friendly Flask + MySQL REST API. No frontend is included.

## Requirements

- Python 3.10 or newer
- MySQL Server
- Postman (optional, for API testing)

## Setup

Create a MySQL database before starting the app:

```sql
CREATE DATABASE employee_db;
```

The MySQL user must have permission to create tables and read/write data in this
database. Set the connection variables in the same terminal where you run the
app. The password is read from the environment and is not stored in the source.

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:MYSQL_HOST = "localhost"
$env:MYSQL_PORT = "3306"
$env:MYSQL_USER = "your_mysql_user"
$env:MYSQL_PASSWORD = "your_mysql_password"
$env:MYSQL_DATABASE = "employee_db"
python app.py
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=your_mysql_user
export MYSQL_PASSWORD=your_mysql_password
export MYSQL_DATABASE=employee_db
python app.py
```

The API runs at `http://127.0.0.1:5000`. The `employees` table is created
automatically when the app starts. The existing SQLite file, if present, is not
imported into MySQL; migrate its data separately if you need to keep it.

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/employees` | List all employees |
| GET | `/employees/1` | Get employee with ID 1 |
| POST | `/employees` | Create employee |
| PUT | `/employees/1` | Replace employee fields |
| DELETE | `/employees/1` | Delete employee |

## Test in Postman

For POST and PUT, select **Body → raw → JSON** and use this sample:

```json
{
  "name": "Ravi Kumar",
  "email": "ravi@example.com",
  "department": "Engineering",
  "salary": 65000
}
```

Send a `POST` request to `http://127.0.0.1:5000/employees`.
Expected result: `201 Created`, with the created employee and its ID.

Then try:
1. `GET http://127.0.0.1:5000/employees`
2. `GET http://127.0.0.1:5000/employees/1`
3. `PUT http://127.0.0.1:5000/employees/1` with all fields in JSON
4. `DELETE http://127.0.0.1:5000/employees/1`

Use a different email for each employee because email addresses must be unique.

## What to learn from this project

- Flask routes and HTTP methods
- JSON request/response handling
- CRUD operations
- SQL queries and parameterized statements
- Validation and HTTP status codes
- Separating database code from route handlers

## Before using in production

This is a learning demo, not production-hardened software. Add automated tests, stronger email validation, structured logging, configuration via environment variables, authentication/authorization, migrations, and a production WSGI server. Do not run Flask's debug server in production.
