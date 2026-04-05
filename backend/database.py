import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'emergency.db')

def get_connection():
    """Returns a database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates all tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS first_aid (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            condition   TEXT NOT NULL,
            steps       TEXT NOT NULL,
            language    TEXT NOT NULL DEFAULT 'en'
        );

        CREATE TABLE IF NOT EXISTS shelters (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            address     TEXT,
            city        TEXT,
            capacity    INTEGER,
            lat         REAL,
            lng         REAL
        );

        CREATE TABLE IF NOT EXISTS evacuation_routes (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            disaster_type   TEXT NOT NULL,
            region          TEXT,
            instructions    TEXT NOT NULL,
            language        TEXT NOT NULL DEFAULT 'en'
        );
    ''')

    conn.commit()
    conn.close()
    print("Tables created successfully.")

def search_first_aid(condition: str, language: str = 'en'):
    """Searches first_aid table by condition keyword and language."""
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        'SELECT * FROM first_aid WHERE condition LIKE ? AND language = ?',
        (f'%{condition}%', language)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_shelters(city: str = ''):
    """Returns shelters filtered by city name."""
    conn = get_connection()
    cursor = conn.cursor()
    if city:
        rows = cursor.execute(
            'SELECT * FROM shelters WHERE city LIKE ?',
            (f'%{city}%',)
        ).fetchall()
    else:
        rows = cursor.execute('SELECT * FROM shelters').fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_evacuation(disaster_type: str, language: str = 'en'):
    """Returns evacuation instructions for a given disaster type."""
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        'SELECT * FROM evacuation_routes WHERE disaster_type = ? AND language = ?',
        (disaster_type, language)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]