import sqlite3
import hashlib

DB_PATH = "HospitalDB.db"

def get_connection():
    """Returns a new connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def initialize_db():
    """Initializes necessary tables that might be missing."""
    conn = get_connection()
    cursor = conn.cursor()
    # Create an admin table for fallback login if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            account_name VARCHAR(100)
        )
    ''')
    # Add a default admin account for local fallback if it doesn't exist
    default_pass = hashlib.md5(b"admin:admin").hexdigest()
    cursor.execute("INSERT OR IGNORE INTO admin (username, password, account_name) VALUES (?, ?, ?)",
                   ('admin', default_pass, 'admin'))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully.")
