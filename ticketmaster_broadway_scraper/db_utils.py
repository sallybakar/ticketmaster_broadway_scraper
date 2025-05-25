import sqlite3

DB_NAME = "broadway_shows.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            show_title TEXT,
            show_date TEXT,
            performance TEXT,
            theatre_name TEXT,
            show_image_link TEXT,
            show_type TEXT,
            details_link TEXT,
            inserted_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_show(row):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Check for duplicates before inserting (based on show_title & show_date)
    c.execute('''
        SELECT id FROM shows WHERE show_title = ? AND show_date = ?
    ''', (row[0], row[1]))
    if c.fetchone():
        conn.close()
        return  # Skip insert if duplicate found

    c.execute('''
        INSERT INTO shows (
            show_title, show_date, performance, theatre_name,
            show_image_link, show_type, details_link, inserted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', row)
    conn.commit()
    conn.close()