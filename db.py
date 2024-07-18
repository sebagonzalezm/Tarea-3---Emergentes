import sqlite3
import uuid

DATABASE_NAME = "games.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS admin(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS company(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            company_api_key TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS location(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            location_name TEXT NOT NULL,
            location_country TEXT NOT NULL,
            location_city TEXT NOT NULL,
            location_meta TEXT,
            FOREIGN KEY (company_id) REFERENCES company(id)
        )""",
        """CREATE TABLE IF NOT EXISTS sensor(
            sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER NOT NULL,
            sensor_name TEXT NOT NULL,
            sensor_category TEXT NOT NULL,
            sensor_meta TEXT,
            sensor_api_key TEXT NOT NULL,
            FOREIGN KEY (location_id) REFERENCES location(id)
        )""",
        """CREATE TABLE IF NOT EXISTS sensor_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY (sensor_id) REFERENCES sensor(sensor_id)
        )"""
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
    db.commit()
    create_default_admin()

def create_default_admin():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM admin WHERE username = ?", ('username',))
    admin = cursor.fetchone()
    if admin is None:
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('username', 'password'))
        db.commit()
        
def generate_api_key():
    return str(uuid.uuid4())
