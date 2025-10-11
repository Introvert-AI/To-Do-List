Todo List App 📝
Deskripsi (Bahasa Indonesia)

Todo List ini adalah aplikasi full-stack sederhana untuk membantu kamu mencatat, membagikan, dan mengelola tugas harian dengan akun pribadi.
Fitur utama meliputi:
- Menambahkan, mengubah, dan menghapus tugas
- Menandai tugas selesai/belum selesai (toggle)
- Sistem register & login akun dengan keamanan token (JWT)
- Komentar dan like di setiap tugas
- Melihat dan mengunjungi halaman tugas milik pengguna lain
- Mengatur visibility (publik atau pribadi) untuk setiap task
- Otentikasi & otorisasi pengguna secara otomatis

## Apa yang Baru? ##
Update kali ini membawa fitur sosial dan keamanan penuh, menjadikan aplikasi ini lebih dari sekadar to-do list pribadi:
- Sistem komentar dan like antar pengguna
- Dashboard pribadi dan dashboard pengguna lain
- Fitur pengaturan visibilitas tugas
- Penanganan error di seluruh frontend agar lebih stabil

Pembersihan struktur proyek dan pemisahan file per fungsi (API, Auth, Frontend)
Teknologi yang Digunakan
Frontend: Streamlit
Backend: FastAPI
Database: SQLite3
Keamanan: Bcrypt (hash password) & JWT (token login)
HTTP Requests: Requests Library

Instalasi & Cara Menjalankan
1. Clone repository:
    git clone https://github.com/Introvert-AI/To-Do-List.git
    cd To-Do-List
2. Install dependencies:
    pip install -r requirements.txt
3. Jalankan API Backend terlebih dahulu:
    uvicorn API.MAINAPI:app --reload
4. Jalankan Frontend Streamlit:
    streamlit run main.py

Description (English)

This Todo List app is a simple full-stack application that helps you create, manage, and share your daily tasks with a personal account.
Main features include:
- Add, edit, and delete tasks
- Toggle task completion status
- Secure account registration & login with JWT tokens
- Comment and like system on tasks
- View other users’ dashboards
- Control visibility (public/private) for each task
- Improved error handling and modular code structure

## What's New? ##
This update introduces social features and secure authentication, transforming the app from a basic local list into a connected system:
- Comment & like system
- Personal and other users’ dashboards
- Task visibility control
- Full error handling
- Clean project structure with separated API & frontend files

Built With
Frontend: Streamlit
Backend: FastAPI
Database: SQLite3
Security: Bcrypt (password hashing), JWT (login token)
Requests Handling: Python requests

Installation & How to Run
1. Clone the repository:
    git clone https://github.com/Introvert-AI/To-Do-List.git
    cd To-Do-List
2. Install dependencies:
    pip install -r requirements.txt
3. Run backend API:
    uvicorn API.MAINAPI:app --reload
4. Run frontend app:
    streamlit run main.py