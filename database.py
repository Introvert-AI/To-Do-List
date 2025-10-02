import sqlite3

def global_connection():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_log():
    conn = global_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS account_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        pw_hash TEXT NOT NULL,
        age INTEGER,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    conn.commit()

def init_data():
    conn = global_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS task_data(
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        status TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES data_login(id) 
    )
                   """)
    conn.commit()
    
# def tampilkan_hasil():
#     conn = global_connection()
#     cursor = conn.cursor()
#     cursor.execute("""SELECT data_login.username, data_login.usia, data_login.password, data_user.tugas, data_user.status
#                    FROM data_login
#                    JOIN data_user ON data_login.id = data_user.user_id""")
#     return cursor.fetchall()
