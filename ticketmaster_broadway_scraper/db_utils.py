import sqlite3

def create_connection():
    return sqlite3.connect("broadway_shows.db")

def create_table():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date TEXT,
            time TEXT,
            venue TEXT,
            image TEXT,
            type TEXT,
            link TEXT,
            scraped_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_show(data):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO shows (title, date, time, venue, image, type, link, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()