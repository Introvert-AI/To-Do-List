from psycopg2.extras import RealDictCursor
import psycopg2

def global_connection():
    conn = psycopg2.connect(
        dbname = "todo_list_db",
        user= "postgres",
        password= "syariff2026",
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor
    )
    return conn
