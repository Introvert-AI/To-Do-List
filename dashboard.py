import streamlit as st
import requests
from account import check_account

def dashboard():
    st.markdown("<h1 style='text-align:center;'>To-Do List</h1>", unsafe_allow_html=True)
    
    check_account()

    if "user_id" not in st.session_state:
        st.warning("Anda harus login dulu!")
        st.stop()

    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    current_user = st.session_state.current_user 
    token =  st.session_state.token[current_user]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Form tambah task
    with st.form("Task"):
        task_input = st.text_input("Tambah task")
        tambah = st.form_submit_button("Tambah")
    
    if tambah:
        if not task_input:
            st.warning("Tugas tidak boleh kosong")
        else:
            response = requests.post("http://127.0.0.1:8000/todolist/addtask",
                                     json={"task": task_input, "status": "Belum Selesai"},
                                     headers=headers)
            if response.status_code in [200,201]:
                st.success("Tugas berhasil ditambahkan!")
                st.rerun()
            else:
                st.error(f"Gagal menambahkan task: {response.text}")

    # Daftar task
    response = requests.get("http://127.0.0.1:8000/todolist/getalltask", headers=headers)
    if response.status_code == 200:
        tasks = response.json()["task"]
        st.markdown("<h3 style='text-align:center;'>📋 Daftar Tugas 📋</h3>", unsafe_allow_html=True)
        for t in tasks:
            task_id = t["task_id"]
            task_name = t["task"]
            status = t["status"]
            col1, col2, col3, col4 = st.columns([3,1,1,1])

            with col1:
                if st.session_state.edit_id == task_id:
                    new_name = st.text_input("Nama task", value=task_name, key=f"input_{task_id}")
                    if st.button("Simpan", key=f"simpan_{task_id}"):
                        response = requests.put(
                            f"http://127.0.0.1:8000/todolist/updatenametask/{task_id}",
                            params={"nama_baru": new_name},
                            headers=headers
                        )
                        if response.status_code == 200:
                            st.session_state.edit_id = None
                            st.rerun()
                        else:
                            st.error(f"Gagal mengubah task: {response.text}")
                    if st.button("Batal", key=f"batal_{task_id}"):
                        st.session_state.edit_id = None
                        st.rerun()
                else:
                    st.write(f"{task_name} - ({status})")

            with col2:
                if st.button("Ubah", key=f"ubah_{task_id}"):
                    st.session_state.edit_id = task_id
                    st.rerun()
            
            with col3:
                if st.button("Toggle", key=f"toggle_{task_id}"):
                    response = requests.put(f"http://127.0.0.1:8000/todolist/updatestatustask/{task_id}",
                                            headers=headers)
                    if response.status_code == 200:
                        st.rerun()
                    else:
                        st.error(f"Gagal mengubah status task: {response.text}")
            
            with col4:
                if st.button("❌", key=f"hapus_{task_id}"):
                    response = requests.delete(f"http://127.0.0.1:8000/todolist/deletetask/{task_id}",
                                               headers=headers)
                    if response.status_code == 200:
                        st.rerun()
                    else:
                        st.error(f"Gagal menghapus task: {response.text}")

    else:
        st.error(f"Gagal ambil data task: {response.text}")
