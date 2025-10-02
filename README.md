# Todo List App 📝

## Deskripsi (Bahasa Indonesia)

Todo List ini adalah aplikasi sederhana untuk membantu kamu mencatat dan mengatur tugas sehari-hari.  
Fitur utama meliputi:
- Menambahkan tugas baru
- Menandai tugas yang sudah selesai dengan toggle
- Menghapus tugas
- Menyimpan data secara lokal di file baru
- Mengubah nama tugas

## Apa yang Baru?

Update ini fokus pada **backend**, karena versi sebelumnya hanya menggunakan database sederhana (one-table) dan bisa diakses tanpa API.  
Fitur-fitur baru yang ditambahkan:
- Sistem register dan login akun
- Sidebar menampilkan informasi akun dan tombol log-out
- API sederhana untuk mengakses database
- Penambahan fitur keamanan: hash password (bcrypt) dan token login (JWT)

## Teknologi yang Digunakan

- **Frontend:** Streamlit
- **Backend:** SQLite3, FastAPI
- **Keamanan:** Bcrypt (hash password), JWT (token login)

## Instalasi & Cara Menjalankan

1. Clone repository:
   ```bash
   git clone https://github.com/Introvert-AI/To-Do-List.git
   cd To-Do-List
2. Install dependencies:
    pip install -r requirements.txt
3. Jalankan aplikasi:
    streamlit run app.py

Description (English)

This Todo List app is a simple application to help you organize and track your daily tasks.
Main features include:
- Add new tasks
- Mark tasks as completed with a toggle
- Delete tasks
- Save data locally
- Edit task names

## What's New? ##
This update focuses on the backend, as the previous version only used a one-table database without API access.
New features:
- Account registration and login
- Sidebar displaying account information and log-out button
- Simple API for database access
- Security features: password hashing (bcrypt) and login token (JWT)

Built With
- Frontend: Streamlit
- Backend: SQLite3, FastAPI
- Security: Bcrypt (password hashing), JWT (login token)

Installation & How to Run
1. Clone the repository:
    git clone https://github.com/Introvert-AI/To-Do-List.git
    cd To-Do-List
2. Install dependencies:
    pip install -r requirements.txt
3. Run the app:
    streamlit run app.py
