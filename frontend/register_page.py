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
            today = datetime.date.today()
            age = today.year - umur_raw.year - ((today.month, today.day) < (umur_raw.month, umur_raw.day))
            print("DEBUG: Hitung umur =", age)

            if age <= 12:
                st.warning("Usia minimal 13 tahun")
            else:
                # Register akun
                print("DEBUG: Mengirim data register ke API")
                response = requests.post(
                    "http://127.0.0.1:8000/account/register",
                    json={
                        "username": username.strip(),
                        "password": password.strip(),
                        "age": age
                    }
                )
                print("DEBUG: Response status_code =", response.status_code)
                print("DEBUG: Response text =", response.text)

                # Langsung ambil JSON, kalau error akan keluar mentah
                response_data = response.json()
                print("DEBUG: Response JSON =", response_data)

                # Login otomatis
                print("DEBUG: Mengirim data login otomatis ke API")
                login_response = requests.post(
                    "http://127.0.0.1:8000/account/login",
                    json={
                        "username": username.strip(),
                        "password": password.strip()
                    }
                )
                login_data = login_response.json()
                print("DEBUG: Login response JSON =", login_data)

                # Ambil token langsung, error kalau field tidak ada
                token = login_data["access_token"]
                print("DEBUG: Token didapat =", token)

                if "token" not in st.session_state:
                    st.session_state.token = {}
                st.session_state.token[username] = token

                st.session_state.current_user = username
                st.session_state.user_id = login_data.get("user_id")
                st.session_state.logged_in = True
                st.session_state.page = "dashboard"
                st.rerun()

    st.write("Sudah punya akun?")
    if st.button("Click Here to Login"):
        st.session_state.page = "login"
        st.rerun()
