import streamlit as st
import sqlite3

@st.cache_resource
def global_connection():
    return sqlite3.connect("todo.db",check_same_thread=False)

def init_db():
    conn = global_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS daftar_tugas (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tugas TEXT,
                       status TEXT
                   )
                   """)
    conn.commit()
    
def tambah_tugas(tugas, status):
    if not tugas:
        return False
    try:
        conn = global_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO daftar_tugas (tugas,status) VALUES (?,?)", (tugas,status))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    
def tampilkan_tugas():
    conn = global_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daftar_tugas")
    data = cursor.fetchall()
    return data

def ubah_status(id_tugas):
    conn = global_connection()
    cursor = conn.cursor()
    #ini baru gua dpt
    #ambil status skrg
    cursor.execute("SELECT status FROM daftar_tugas WHERE id = ?", (id_tugas,))
    current_status = cursor.fetchone()[0]
    
    #tentukan status baru
    status_baru = "Selesai" if current_status != "Selesai" else "Belum Selesai"
    
    #update ke Database
    cursor.execute("UPDATE daftar_tugas SET status= ? WHERE id= ?",(status_baru,id_tugas))
    conn.commit()

    return status_baru

def update_tugas(nama_baru,id_tugas):
    conn = global_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE daftar_tugas SET tugas= ? WHERE id= ?", (nama_baru,id_tugas))
    conn.commit()
    
def hapus_tugas(id_tugas):
    conn = global_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daftar_tugas WHERE id = ?",(id_tugas,))
    conn.commit()
