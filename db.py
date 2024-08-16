# File to handle database connection and setup in application
import sqlite3

# Establishes and returns a connection to SQLite
def get_db_connection():
    conn = sqlite3.connect('users.db')  # opens connection to database file name 'users'
    conn.row_factory = sqlite3.Row   # rows returned by queries behave like dictionaries
    return conn

# Initializes database by creating necessary tables
def setup_database():
    conn = get_db_connection()   # establish connection to db
    cursor = conn.cursor()       # creates cursor object to execute SQL queries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            if INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
