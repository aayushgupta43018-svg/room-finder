# import mysql.connector

# def get_db_connection():
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="password",
#         database="room_rental_db"
#     )
#     return connection

import os
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ["DB_PASSWORD"],
        database=os.environ.get("DB_NAME", "room_rental_db")
    )
    return connection
