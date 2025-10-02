import streamlit as st
import datetime
import requests

def register_account():
    st.markdown("<h3 style='text-align:center;'> Halaman Daftar Akun </h3>", unsafe_allow_html=True)
    if "token" not in st.session_state or st.session_state.token is None:
            st.session_state.token = {}
            
    min_date = datetime.date(1900, 1, 1)
    max_date = datetime.date.today()
    
    with st.form("Daftar Akun"):
        username = st.text_input("Username")
        umur_raw = st.date_input("Tanggal Lahir", value=datetime.date(2000, 1, 1),
                                 min_value=min_date, max_value=max_date)
        password = st.text_input("Password", type="password")
        daftar = st.form_submit_button("Daftar")
    
    if daftar:
        if not username.strip() or not password.strip():
            st.warning("Username dan password tidak boleh kosong")
        else:
            try:
                today = datetime.date.today()
                age = today.year - umur_raw.year - ((today.month, today.day) < (umur_raw.month, umur_raw.day))
                
                if age <= 12:
                    st.warning("Usia minimal 13 tahun")
                else:
                    # Register akun
                    response = requests.post(
                        "http://127.0.0.1:8000/todolist/account/register",
                        json={
                            "username": username.strip(),
                            "password": password.strip(),
                            "age": int(age)
                        }
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.success("Akun berhasil dibuat! Login otomatis...")

                        # Login otomatis
                        login_response = requests.post(
                            "http://127.0.0.1:8000/todolist/account/login",
                            json={
                                "username": username.strip(),
                                "password": password.strip()
                            }
                        )

                        if login_response.status_code == 200:
                            token = login_response.json()["access_token"]

                            # Simpan token per username
                            if "token" not in st.session_state:
                                st.session_state.token = {}
                            st.session_state.token[username] = token

                            # Set current user
                            st.session_state.current_user = username
                            st.session_state.user_id = login_response.json().get("user_id")
                            st.session_state.logged_in = True
                            st.session_state.page = "dashboard"
                            st.rerun()
                        else:
                            try:
                                err = login_response.json().get("detail") or login_response.text
                            except:
                                err = login_response.text
                            st.error(f"Login otomatis gagal: {err}")
                    else:
                        try:
                            err = response.json().get("detail") or response.text
                        except:
                            err = response.text
                        st.error(f"Register gagal: {err}")
            except requests.exceptions.RequestException as e:
                st.error(f"Tidak bisa terhubung ke server: {e}")

    st.write("Sudah punya akun?")
    if st.button("Click Here to Login"):
        st.session_state.page = "login"
        st.rerun()
