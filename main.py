import streamlit as st
from frontend.register_page import register_account
from frontend.login_page import login_account
from frontend.main_page import dashboard
from frontend.all_account_page import all_account
from frontend.other_user_page import other_dashboard

# Inisialisasi session_state
if "token" not in st.session_state:
    st.session_state.token = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page" not in st.session_state:
    st.session_state.page = "register"

# Routing
if st.session_state.page == "dashboard":
    dashboard()
elif st.session_state.page == "dashboard_other":
    other_dashboard()
elif st.session_state.page == "new_page":
    all_account()
elif st.session_state.page == "register":
    register_account()
elif st.session_state.page == "login":
    login_account()
    
