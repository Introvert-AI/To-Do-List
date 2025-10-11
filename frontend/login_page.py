import streamlit as st
import requests

def login_account():
    st.markdown("<h1 style='text-align:center;'>Halaman Login</h1>", unsafe_allow_html=True)
    if "token" not in st.session_state or st.session_state.token is None:
        st.session_state.token = {}
        
    with st.form("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")
    
    if login:
        if not username or not password:
            st.warning("Data tidak boleh kosong")
            return
        
        try:
            response = requests.post("http://127.0.0.1:8000/account/login", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state.token[username] = token
                st.session_state.current_user = username
                st.session_state.user_id = response.json().get("user_id")
                st.session_state.logged_in = True
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                err = response.json().get("detail") or response.text
                st.error(f"Login gagal: {err}")
        except requests.exceptions.RequestException as e:
            st.error(f"Tidak bisa terhubung ke server: {e}")

    st.write("Belum punya akun?")
    if st.button("Click Here to Register"):
        st.session_state.page = "register"
        st.rerun()
