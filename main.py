from backend import init_db, tambah_tugas, tampilkan_tugas, ubah_status, update_tugas, hapus_tugas
import streamlit as st

# Inisialisasi default
init_db()

st.markdown("<h1 style=' text-align: center;'> To-Do List </h1>", unsafe_allow_html=True)

# Input tugas baru
with st.form("b"):
    tugas_baru = st.text_input("Tambah tugas")
    tambah = st.form_submit_button("Tambah")

if tambah:
    tugas = tugas_baru
    status = "belum selesai"
    if tambah_tugas(tugas, status):
        st.success("Berhasil")
    else:
        st.warning("Tugas sudah ada atau kosong")

st.markdown("<h3 style=' text-align: center;'>📋 Daftar Tugas 📋</h1>",unsafe_allow_html=True)
tugas_list = tampilkan_tugas()

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None
    
for t in tugas_list:
    id_tugas, tugas, status = t
    col1, col2, col3, col4= st.columns([3, 1,1,1])
    with col1:
        if st.session_state.edit_id == id_tugas:
            nama_baru = st.text_input("Nama tugas",value=tugas, key=f"input_{id_tugas}")
            if st.button("Simpan",key=f"simpan_{id_tugas}"):
                update_tugas(nama_baru,id_tugas)
                st.session_state.edit_id = None
                st.rerun()
            if st.button("Batal", key=f"batal_{id_tugas}"):
                st.session_state.edit_id = None
                st.rerun
        else:
            st.write(f"{tugas} - ({status})")
    with col2:
        if st.button("Ubah", key=f"ubah_{id_tugas}"):
            st.session_state.edit_id = id_tugas
            st.rerun()
                    
    with col3:
        if st.button("Toggle", key=f"toggle_{id_tugas}"):
            ubah_status(id_tugas)
            st.rerun()
    with col4:
        if st.button("❌", key=f"hapus_{id_tugas}"):
            hapus_tugas(id_tugas)
            st.rerun()
        

