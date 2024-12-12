import sqlite3

def initialize_db():
    """
    Initialize the database with users and messages tables.
    If the tables already exist, they won't be recreated.
    """
    try:
        with sqlite3.connect('encrypt.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            print("[INFO] Database initialized successfully.")

    except sqlite3.Error as e:
        print(f"[ERROR] An error occurred while initializing the database: {e}")

if __name__ == "__main__":
    initialize_db()
