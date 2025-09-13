import streamlit as st

def init_state():
    if "daftar_tugas" not in st.session_state:
        st.session_state.daftar_tugas = []

def tambah_tugas(tugas_baru):
    tugas_baru = tugas_baru.strip()
    if tugas_baru and tugas_baru not in st.session_state.daftar_tugas:
        st.session_state.daftar_tugas.append(tugas_baru)
        return True
    return False

def hapus_tugas(index):
    st.session_state.daftar_tugas.pop(index)
    st.rerun()
