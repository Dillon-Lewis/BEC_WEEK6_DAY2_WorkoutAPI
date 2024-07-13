import mysql.connector
from mysql.connector import Error
import json

db_name = 'ecom'
user = 'root'
password = 'Ziggyjone$3'
host = 'localhost'

def connection():
    '''
    Creates and returns a connection to our database.
    '''
    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None
