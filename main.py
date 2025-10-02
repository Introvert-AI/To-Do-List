import streamlit as st
from register import register_account
from login import login_account
from dashboard import dashboard

# Inisialisasi session_state
if "token" not in st.session_state:
    st.session_state.token = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page" not in st.session_state:
    st.session_state.page = "register"

# Routing
if st.session_state.logged_in:
    dashboard()
else:
    if st.session_state.page == "register":
        register_account()
    elif st.session_state.page == "login":
        login_account()
