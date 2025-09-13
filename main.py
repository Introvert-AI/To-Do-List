from backend import init_state, tambah_tugas, hapus_tugas
import streamlit as st

# Inisialisasi default
init_state()

st.markdown("<h1 style=' text-align: center;'> To-Do List </h1>", unsafe_allow_html=True)

# Input tugas baru
with st.form("b"):
    tugas_baru = st.text_input("Tambah tugas")
    tambah = st.form_submit_button("Tambah")

if tambah:
    if not tambah_tugas(tugas_baru):
        st.warning("Tugas sudah ada atau kosong")

st.write("📋 Daftar Tugas:")

# Loop daftar tugas + bikin tombol hapus
for i, tugas in enumerate(st.session_state.daftar_tugas):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"- {tugas}")
    with col2:
        if st.button("❌", key=f"hapus_{i}"):
            hapus_tugas(i)

# Tombol hapus semua
st.button("Hapus Semua", on_click=lambda: st.session_state.update({"daftar_tugas": []}))

with st.expander("Lihat ini"):
    st.warning("Tekan tombol ini jika ingin mereset semua kegiatan")
