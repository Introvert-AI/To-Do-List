from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from core.database import global_connection
from core.auth import create_access_token, get_current_user
from psycopg2 import errors

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Models
class TaskModel(BaseModel):
    task: str
    status: bool = False


@router.post("/add")
def add_task(data: TaskModel, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO tasks (task, status, user_id) VALUES (%s,%s,%s)",
                (data.task, data.status, current_user["id"]),
            )
            conn.commit()
            return {"success": True, "message": "Tugas berhasil ditambahkan"}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))


# @router.get("/")
# def get_all_tasks(current_user: dict = Depends(get_current_user)):
#     with global_connection() as conn:
#         cur = conn.cursor()

#         if current_user["role"] == "admin":
#             cur.execute("""
#                 SELECT id, task, status, visibility, user_id
#                 FROM tasks
#                 ORDER BY id ASC
#             """)
#         else:
#             cur.execute("""
#                 SELECT id, task, status, visibility, user_id
#                 FROM tasks
#                 WHERE user_id=%s OR visibility = TRUE
#                 ORDER BY id ASC
#             """, (current_user["id"],))

#         rows = cur.fetchall()

#     tasks = [
#         {
#             "id": row["id"],
#             "task": row["task"],
#             "status": row["status"],
#             "visibility": row["visibility"],
#             "user_id": row["user_id"],
#         }
#         for row in rows
#     ]
#     return {"tasks": tasks}

@router.get("/")
def get_all_tasks(current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, task, status, visibility, user_id
            FROM tasks
            WHERE user_id=%s ORDER BY id ASC
        """, (current_user["id"],))
 
        rows = cur.fetchall()

    tasks = [
        {
            "id": row["id"],
            "task": row["task"],
            "status": row["status"],
            "visibility": row["visibility"],
            "user_id": row["user_id"],
        }
        for row in rows
    ]
    return {"tasks": tasks}


@router.put("/update-name/{task_id}")
def update_task(nama_baru: str, task_id: int, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE tasks SET task=%s WHERE id=%s AND user_id=%s",
            (nama_baru, task_id, current_user["id"]),
        )
        conn.commit()

        if cur.rowcount > 0:
            return {"success": True, "message": "Tugas berhasil diubah"}
        return {"success": False, "message": "Tugas tidak ditemukan"}


@router.put("/update-status/{task_id}")
def status_change(task_id: int, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT status FROM tasks WHERE id=%s AND user_id=%s", (task_id, current_user["id"]))
        row = cur.fetchone()

        if not row:
            return {"success": False, "message": "Tugas tidak ditemukan"}

        current_status = row["status"]
        new_status = not current_status

        cur.execute(
            "UPDATE tasks SET status=%s WHERE id=%s AND user_id=%s",
            (new_status, task_id, current_user["id"]),
        )
        conn.commit()

        return {"success": True, "message": f"Status task diubah ke {new_status}"}


@router.delete("/delete/{task_id}")
def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=%s AND user_id=%s", (task_id, current_user["id"]))
        conn.commit()

        if cur.rowcount > 0:
            return {"success": True, "message": "Tugas berhasil dihapus"}
        return {"success": False, "message": "Tugas tidak ditemukan"}

# --- Visibility ---
@router.put("/setvisibility/{task_id}")
def change_visibility(task_id: int, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        with conn.cursor() as cur:
            # toggle visibility: dari True jadi False, dari False jadi True
            cur.execute("""
                UPDATE tasks
                SET visibility = NOT visibility
                WHERE id = %s AND user_id = %s
                RETURNING visibility
            """, (task_id, current_user["id"]))
            result = cur.fetchone()
        conn.commit()

    if result:
        return {"success": True, "new_visibility": result["visibility"]}
    else:
        return {"success": False, "message": "Task tidak ditemukan atau bukan milik user"}
