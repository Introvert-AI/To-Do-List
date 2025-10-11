import streamlit as st
import requests
from frontend.account import check_my_account
from datetime import datetime, timezone

def time_ago(ts):
    if isinstance(ts, str):
        ts = datetime.fromisoformat(ts)
    now = datetime.now()
    diff = now - ts
    seconds = diff.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} detik lalu"
    elif seconds < 3600:
        return f"{int(seconds//60)} menit lalu"
    elif seconds < 86400:
        return f"{int(seconds//3600)} jam lalu"
    else:
        return f"{int(seconds//86400)} hari lalu"


def dashboard():
    st.markdown("<h1 style='text-align:center;'>To-Do List</h1>", unsafe_allow_html=True)
    check_my_account()

    if "user_id" not in st.session_state:
        st.warning("Anda harus login dulu!")
        st.stop()

    if "edit_id" not in st.session_state:
        st.session_state.edit_id = None

    current_user = st.session_state.current_user 
    token = st.session_state.token[current_user]
    headers = {"Authorization": f"Bearer {token}"}

    # === Form tambah task ===
    with st.form("Task"):
        task_input = st.text_input("Tambah task")
        tambah = st.form_submit_button("Tambah")

    if tambah:
        if not task_input:
            st.warning("Tugas tidak boleh kosong")
        else:
            response = requests.post(
                "http://127.0.0.1:8000/tasks/add",
                json={"task": task_input, "status": False},
                headers=headers
            )
            if response.status_code in [200, 201]:
                st.success("Tugas berhasil ditambahkan!")
                st.rerun()
            else:
                st.error(f"Gagal menambahkan task: {response.text}")

    # === Daftar task ===
    response = requests.get("http://127.0.0.1:8000/tasks", headers=headers)
    if response.status_code == 200:
        tasks = response.json()["tasks"]
        st.markdown("<h3 style='text-align:center;'>📋 Daftar Tugas 📋</h3>", unsafe_allow_html=True)
        for t in tasks:
            task_id = t["id"]
            task_name = t["task"]
            status = t["status"]
            task_owner_id = t["user_id"]  # pastikan field ini dikembalikan oleh API

            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

            with col1:
                if st.session_state.edit_id == task_id:
                    new_name = st.text_input("Nama task", value=task_name, key=f"input_{task_id}")
                    if st.button("Simpan", key=f"simpan_{task_id}"):
                        response = requests.put(
                            f"http://127.0.0.1:8000/tasks/update-name/{task_id}",
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
                    status_label = "Selesai" if status else "Belum Selesai"
                    st.write(f"{task_name} - ({status_label})")

                    # === Komentar & Likes ===
                    with st.expander("Komentar & Likes"):
                        response = requests.get(f"http://127.0.0.1:8000/comment/{task_id}", headers=headers)
                        st.markdown("**💬 Komentar:**")
                        if response.status_code == 200:
                            comments = response.json()["comments"]
                            if comments:
                                for c in comments:
                                    comment_id = c["id"]
                                    comment = c["comment"]
                                    author = c["author_username"]
                                    st.write(f"- {comment} *(oleh {author})*")
                                    if st.button("❌", key=f"hapus_komen_{comment_id}"):
                                        response = requests.delete(
                                            f"http://127.0.0.1:8000/comment/delete/{comment_id}",
                                            headers=headers
                                        )
                                        if response.status_code == 200:
                                            st.rerun()
                                        else:
                                            st.error(f"Gagal menghapus komen: {response.text}")
                            else:
                                st.info("Belum ada komentar")
                        else:
                            st.error(f"Gagal mengambil komentar: {response.text}")

                        # Form tambah komentar
                        with st.form(f"comments_{task_id}"):
                            new_comment = st.text_input("Comment :")
                            submit = st.form_submit_button("Submit")
                            if submit:
                                response = requests.post(
                                    f"http://127.0.0.1:8000/comment/add/{task_id}",
                                    json={"comment": new_comment},
                                    headers=headers
                                )
                                if response.status_code == 200:
                                    st.rerun()
                                else:
                                    st.error(f"Gagal mengirim komen: {response.text}")

                        # Jumlah like
                        like_count_res = requests.get(f"http://127.0.0.1:8000/like/count/{task_id}", headers=headers)
                        like_count = like_count_res.json()["total_likes"] if like_count_res.status_code == 200 else 0

                        # Status like user
                        status_res = requests.get(f"http://127.0.0.1:8000/like/status/{task_id}", headers=headers)
                        liked = status_res.json().get("liked", False) if status_res.status_code == 200 else False

                        # Tombol like
                        like_text = "❤️ Liked" if liked else "🤍 Like"
                        if st.button(like_text, key=f"like_{task_id}"):
                            toggle_res = requests.post(f"http://127.0.0.1:8000/like/add{task_id}", headers=headers)
                            if toggle_res.status_code == 200:
                                st.rerun()

                        st.write(f"{like_count} likes")

                        # Lihat semua user yang like
                        users_res = requests.get(f"http://127.0.0.1:8000/like/users/{task_id}", headers=headers)
                        if users_res.status_code == 200:
                            users = users_res.json()
                            if users:
                                st.markdown("**👥 Lihat semua yang like:**")
                                for u in users:
                                    st.write(f"- {u['username']} ({time_ago(u['create_at'])})")

            # === Tombol Aksi ===
            with col2:
                if st.button("Ubah", key=f"ubah_{task_id}"):
                    st.session_state.edit_id = task_id
                    st.rerun()

            with col3:
                if st.button("Toggle", key=f"toggle_status_{task_id}"):
                    response = requests.put(f"http://127.0.0.1:8000/tasks/update-status/{task_id}", headers=headers)
                    if response.status_code == 200:
                        st.rerun()
                    else:
                        st.error(f"Gagal mengubah status task: {response.text}")

            with col4:
                if st.button("❌", key=f"hapus_{task_id}"):
                    response = requests.delete(f"http://127.0.0.1:8000/tasks/delete/{task_id}", headers=headers)
                    if response.status_code == 200:
                        st.rerun()
                    else:
                        st.error(f"Gagal menghapus task: {response.text}")

            with col5:
                if task_owner_id == st.session_state["user_id"]:
                    visibility = t.get("visibility", False)
                    icon = "👁️" if visibility else "🙈"

                    # Key harus unik dan statis
                    button_key = f"visibility_btn_{task_id}"

                    if st.button(icon, key=button_key):
                        try:
                            res = requests.put(
                                f"http://127.0.0.1:8000/tasks/setvisibility/{task_id}",
                                headers=headers
                                )
                            if res.status_code == 200:
                                new_vis = res.json().get("new_visibility", None)
                                st.toast(f"Visibility task #{task_id} → {new_vis}")
                                st.rerun()
                            else:
                                st.error(f"Gagal ubah visibility: {res.text}")
                        except Exception as e:
                            st.error(f"Error toggle visibility: {e}")



    else:
        st.error(f"Gagal ambil data task: {response.text}")
