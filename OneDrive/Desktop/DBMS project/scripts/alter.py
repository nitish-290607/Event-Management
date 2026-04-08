import sqlite3

def alter_db():
    try:
        conn = sqlite3.connect('event_management.db')
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE events ADD COLUMN ticket_price FLOAT DEFAULT 100.0")
        conn.commit()
        print("Column ticket_price added successfully.")
    except Exception as e:
        print("Error or already added:", str(e))
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    alter_db()
