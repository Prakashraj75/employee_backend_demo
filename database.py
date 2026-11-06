import os

import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.environ["MYSQL_PASSWORD"],
        database=os.getenv("MYSQL_DATABASE", "employee_db")
    )


def init_db():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                department VARCHAR(255) NOT NULL,
                salary DOUBLE NOT NULL CHECK (salary >= 0)
            )
            """
        )
        connection.commit()
        print("Employees table created successfully.")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    init_db()
    print("MySQL database ready.")
