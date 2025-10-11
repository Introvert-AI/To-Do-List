import streamlit as st
import requests

def all_account():
    st.markdown("<h1 style='text-align:center;'>To-Do List</h1>", unsafe_allow_html=True)
    
    current_user = st.session_state.current_user 
    token = st.session_state.token[current_user]
    headers = {"Authorization": f"Bearer {token}"}
    
    st.header("Layout account")
    response = requests.get("http://127.0.0.1:8000/account/info/all", headers=headers)
    if response.status_code == 200:
        accounts = response.json()["all_account"]
        for username in accounts:
            if username == current_user:
                continue  # 🟩 jangan tampilkan akun sendiri

            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"👤 {username}")
            with col2:
                # 🟩 ubah ke sistem navigasi dashboard user lain
                if st.button("Kunjungi", key=f"visit_{username}"):
                    st.session_state.selected_user = username
                    st.session_state.page = "dashboard_other"  # 🟩 ganti ke page khusus
                    st.rerun()
    
    if st.button("Kembali", key="Kembali_sidebar"):
        if current_user in st.session_state.token:
            st.session_state.page = "dashboard"
            st.rerun()
