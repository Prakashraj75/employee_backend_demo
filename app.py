from flask import Flask, jsonify, request
from database import init_db, get_db_connection
from mysql.connector import IntegrityError

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({
        "message": "Employee Management API",
        "status": "running",
        "endpoints": [
            "GET /employees",
            "GET /employees/<id>",
            "POST /employees",
            "PUT /employees/<id>",
            "DELETE /employees/<id>"
        ]
    })


@app.get("/employees")
def list_employees():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, name, email, department, salary FROM employees ORDER BY id"
        )
        employees = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    return jsonify(employees), 200


@app.get("/employees/<int:employee_id>")
def get_employee(employee_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, name, email, department, salary FROM employees WHERE id = %s",
            (employee_id,)
        )
        employee = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify(dict(employee)), 200


@app.post("/employees")
def create_employee():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    required_fields = ["name", "email", "department", "salary"]
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] in (None, "")
    ]
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    try:
        name = str(data["name"]).strip()
        email = str(data["email"]).strip().lower()
        department = str(data["department"]).strip()
        salary = float(data["salary"])
    except (TypeError, ValueError):
        return jsonify({"error": "Salary must be a valid number"}), 400

    if not name or not email or not department:
        return jsonify({"error": "Name, email, and department cannot be blank"}), 400
    if "@" not in email:
        return jsonify({"error": "Email address is invalid"}), 400
    if salary < 0:
        return jsonify({"error": "Salary cannot be negative"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            INSERT INTO employees (name, email, department, salary)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, department, salary)
        )
        connection.commit()
        employee_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, name, email, department, salary FROM employees WHERE id = %s",
            (employee_id,)
        )
        employee = cursor.fetchone()
    except IntegrityError:
        connection.rollback()
        return jsonify({"error": "Could not create employee. Email may already exist."}), 409
    finally:
        cursor.close()
        connection.close()

    if employee is None:
        return jsonify({"error": "Could not create employee"}), 500

    return jsonify(employee), 201


@app.put("/employees/<int:employee_id>")
def update_employee(employee_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    required_fields = ["name", "email", "department", "salary"]
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] in (None, "")
    ]
    if missing_fields:
        return jsonify({
            "error": "PUT requires all employee fields",
            "fields": missing_fields
        }), 400

    try:
        name = str(data["name"]).strip()
        email = str(data["email"]).strip().lower()
        department = str(data["department"]).strip()
        salary = float(data["salary"])
    except (TypeError, ValueError):
        return jsonify({"error": "Salary must be a valid number"}), 400

    if not name or not email or not department or "@" not in email:
        return jsonify({"error": "Please provide valid name, email, and department"}), 400
    if salary < 0:
        return jsonify({"error": "Salary cannot be negative"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            UPDATE employees
            SET name = %s, email = %s, department = %s, salary = %s
            WHERE id = %s
            """,
            (name, email, department, salary, employee_id)
        )
        cursor.execute(
            "SELECT id, name, email, department, salary FROM employees WHERE id = %s",
            (employee_id,)
        )
        employee = cursor.fetchone()
        if employee is None:
            connection.rollback()
            return jsonify({"error": "Employee not found"}), 404
        connection.commit()
    except IntegrityError:
        connection.rollback()
        return jsonify({"error": "Could not update employee. Email may already exist."}), 409
    finally:
        cursor.close()
        connection.close()
    return jsonify(employee), 200


@app.delete("/employees/<int:employee_id>")
def delete_employee(employee_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        connection.commit()
        rowcount = cursor.rowcount
    finally:
        cursor.close()
        connection.close()

    if rowcount == 0:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": f"Employee {employee_id} deleted successfully"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
