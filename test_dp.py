import mysql.connector
from db import get_db_connection

try:
    connection = get_db_connection()
    print("MySQL connected successfully!")

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")

    print("Tables in database:")

    for table in cursor.fetchall():
        print(table[0])

    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print("Database error:", error)