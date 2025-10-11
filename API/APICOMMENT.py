from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.database import global_connection
from core.auth import get_current_user

class CommentsModel(BaseModel):
    comment: str

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)

# --- Tambah komentar ---
@router.post("/add/{task_id}")
def add_comment(task_id: int, data: CommentsModel, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO comments (comment, author_id, task_id)
                VALUES (%s, %s, %s)
            """, (data.comment, current_user["id"], task_id))
            conn.commit()
    return {"success": True, "message": "Komentar berhasil ditambahkan"}


# --- Ambil semua komentar berdasarkan task_id ---
@router.get("/{task_id}")
def get_comments(task_id: int, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.comment, c.author_id, u.username, c.create_at
                FROM comments c
                JOIN users u ON c.author_id = u.id
                WHERE c.task_id = %s
                ORDER BY c.create_at ASC
            """, (task_id,))
            comments = cur.fetchall()

            result = [
                {
                    "id": c["id"],
                    "comment": c["comment"],
                    "author_id": c["author_id"],
                    "author_username": c["username"],
                    "created_at": c["create_at"]
                }
                for c in comments
            ]
    return {"comments": result}


# --- Hapus komentar (hanya pemilik komentar yang boleh) ---
@router.delete("/delete/{comment_id}")
def delete_comment(comment_id: int, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM comments WHERE id=%s AND author_id=%s",
                (comment_id, current_user["id"])
            )
            conn.commit()
            if cur.rowcount > 0:
                return {"success": True, "message": "Komentar berhasil dihapus"}
            else:
                return {"success": False, "message": "Komentar tidak ditemukan"}
