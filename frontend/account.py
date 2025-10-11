import requests
import streamlit as st


def check_other_account():
    if "user_id" in st.session_state and st.session_state.user_id:
        if "token" not in st.session_state or st.session_state.token is None:
            st.session_state.token = {}
            
        current_user = st.session_state.get("current_user")
        token = st.session_state.token[current_user]
            
        username = st.session_state.selected_user
        headers = {"Authorization": f"Bearer {token}"}
            
        response = requests.get(f"http://127.0.0.1:8000/account/my_info/{username}", headers=headers)

        # Ambil data JSON langsung, error akan muncul jika API gagal
        user = response.json()
            
        with st.sidebar:
            st.markdown("### 👤 Info Akun")
            st.write(f"**Username:** {user['username']}")
            st.write(f"**Usia:** {user['age']} tahun")
            st.write(f"**Password:** ********")
            st.write("---")
            if st.button("Kembali ke halaman utama", key="logout_sidebar"):
                st.session_state.selected_user = None
                st.session_state.page = "dashboard"
                st.rerun()
            if st.button("pindah ke page baru",key="pindah"):
                st.session_state.page = "new_page"
                st.session_state.selected_user = None
                st.rerun()
            
def check_my_account():
    if "user_id" in st.session_state and st.session_state.user_id:
        if "token" not in st.session_state or st.session_state.token is None:
            st.session_state.token = {}

        current_user = st.session_state.get("current_user")
        if not current_user:
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.page = "login"
            st.rerun()
            return

        token = st.session_state.token[current_user]
        if not token:
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.page = "login"
            st.rerun()
            return

        username = st.session_state.current_user
        headers = {"Authorization": f"Bearer {token}"}
        # Request langsung, error akan muncul mentah kalau ada masalah
        response = requests.get(f"http://127.0.0.1:8000/account/my_info/{username}", headers=headers)

        # Ambil data JSON langsung, error akan muncul jika API gagal
        user = response.json()

        # Tampilkan info akun di sidebar
        with st.sidebar:
            st.markdown("### 👤 Info Akun")
            st.write(f"**Username:** {user['username']}")
            st.write(f"**Usia:** {user['age']} tahun")
            st.write(f"**Password:** ********")
            st.write("---")
            if st.button("Logout", key="logout_sidebar"):
                # Hapus token hanya untuk user ini
                if current_user in st.session_state.token:
                    del st.session_state.token[current_user]

                # Reset session state akun ini
                st.session_state.pop(current_user, None)
                st.session_state.current_user = None
                st.session_state.user_id = None
                st.session_state.logged_in = False
                st.session_state.page = "login"
                st.rerun()
            if st.button("pindah ke page baru",key="pindah"):
                st.session_state.page = "new_page"
                st.rerun()