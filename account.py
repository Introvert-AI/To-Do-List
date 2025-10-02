import requests
import streamlit as st

def check_account():
    if "user_id" in st.session_state and st.session_state.user_id:
        if "token" not in st.session_state or st.session_state.token is None:
            st.session_state.token = {}
            
        current_user = st.session_state.get("current_user")
        if not current_user:
            st.warning("Token untuk akun ini tidak ditemukan. Silakan login kembali.")
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.page = "login"
            st.rerun()
            return

        token = st.session_state.token[current_user]
        if not token:
            st.warning("Token untuk akun ini tidak ditemukan. Silakan login kembali.")
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.page = "login"
            st.rerun()
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"http://127.0.0.1:8000/todolist/account/info/", headers=headers)
        
        if response.status_code == 200:
            user = response.json()
            if "error" not in user:
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
                        st.session_state.pop(current_user,None)
                        st.session_state.current_user = None
                        st.session_state.user_id = None
                        st.session_state.logged_in = False
                        st.session_state.page = "login"
                        st.rerun()
            else:
                st.warning("User tidak ditemukan")
        else:
            st.error(f"Gagal ambil data akun: {response.text}")
