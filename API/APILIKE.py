from fastapi import APIRouter, Depends
from core.database import global_connection
from core.auth import get_current_user

router = APIRouter(
    prefix="/like",
    tags=["like"]
)

# --- Likes ---
@router.post("/add/{task_id}")
def like(task_id: int, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        with conn.cursor() as cur:
            # Cek apakah sudah like
            cur.execute("SELECT 1 FROM likes WHERE user_id=%s AND task_id=%s",
                        (current_user["id"], task_id))
            exists = cur.fetchone()
            
            if exists:
                # Sudah like → hapus row (unlike)
                cur.execute("DELETE FROM likes WHERE user_id=%s AND task_id=%s",
                            (current_user["id"], task_id))
                action = "unliked"
            else:
                # Belum like → tambah row
                cur.execute("INSERT INTO likes (user_id, task_id, created_at) VALUES (%s, %s, NOW())",
                            (current_user["id"], task_id))
                action = "liked"
            conn.commit()
    return {"status": action}


@router.get("/count/{task_id}")
def get_like_count(task_id: int):
    with global_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as total FROM likes WHERE task_id=%s", (task_id,))
            total = cur.fetchone()["total"]
    return {"total_likes": total}


@router.get("/status/{task_id}")
def get_like_status(task_id: int, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM likes WHERE task_id=%s AND user_id=%s",
                        (task_id, current_user["id"]))
            liked = cur.fetchone() is not None
    return {"liked": liked}


@router.get("/users/{task_id}")
def get_likes_users(task_id: int):
    with global_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT u.username, l.create_at
                FROM likes l
                JOIN users u ON l.user_id = u.id
                WHERE l.task_id = %s
                ORDER BY l.create_at ASC
            """, (task_id,))
            rows = cur.fetchall()
            result = [{"username": r["username"], "create_at": r["create_at"]} for r in rows]
    return result
