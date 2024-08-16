# Authentication file
import hashlib
import sqlite3
from db import get_db_connection

# Function takes password as a parameter to return an encoded version converted -> bytes -> hexadecimal for storage and comparison
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Handles the registration of new users
def register_user(username, password):
    conn = get_db_connection()    # establishes connection to database
    cursor = conn.cursor()        # creates cursor object to execute SQL queries
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hash_password(password))
    )# inserts the username and hashed password into 'users' table in database
    conn.commit()  # saves changes to the database
    conn.close()   # Close database connection

def login_user(username, password):
    conn = get_db_connection()      # connects to the database
    cursor = conn.cursor()        # Creates cursor object to execute SQL queries
    # Search the 'users' table for a row in which username and hashpassword match the provided credentials
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hash_password(password))
    )
    user = cursor.fetchone()  # fetches first matching row from database,
    conn.close()    # close database connection
    return user