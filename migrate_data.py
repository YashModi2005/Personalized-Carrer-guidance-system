
import sqlite3
import mysql.connector
import os
from dotenv import load_dotenv

# Load MySQL settings
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(env_path)

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'admin123'),
    'database': os.getenv('MYSQL_DATABASE', 'career_pilot_db')
}

SQLITE_PATH = os.path.join('backend', 'career_pilot.db')

def migrate():
    if not os.path.exists(SQLITE_PATH):
        print("SQLite database not found.")
        return

    lite_conn = sqlite3.connect(SQLITE_PATH)
    lite_cursor = lite_conn.cursor()

    my_conn = mysql.connector.connect(**MYSQL_CONFIG)
    my_cursor = my_conn.cursor()

    tables = ['users', 'registrations', 'chats', 'metrics']

    for table in tables:
        print(f"Migrating table: {table}")
        
        # Get column names
        lite_cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in lite_cursor.fetchall()]
        
        if not columns:
            print(f"Skipping {table} (not found in SQLite)")
            continue

        # Fetch data
        lite_cursor.execute(f"SELECT * FROM {table}")
        rows = lite_cursor.fetchall()

        if not rows:
            print(f"No data in {table}")
            continue

        # Prepare MySQL insert
        placeholders = ', '.join(['%s'] * len(columns))
        col_list = ', '.join(columns)
        insert_query = f"INSERT IGNORE INTO {table} ({col_list}) VALUES ({placeholders})"
        
        my_cursor.executemany(insert_query, rows)
        my_conn.commit()
        print(f"Successfully migrated {len(rows)} rows to {table}")

    lite_conn.close()
    my_conn.close()
    print("Migration complete!")

if __name__ == "__main__":
    migrate()
