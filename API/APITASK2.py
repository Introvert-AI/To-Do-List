from core.database import global_connection
from core.auth import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter (
    prefix="/other",
    tags=["other"]
)

@router.get("/{username}")
def get_all_tasks(username:str, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=%s",(username,))
        rows = cur.fetchone()
        
        target_user_id = rows["id"]
        
        cur.execute("""
            SELECT id, task, status, visibility, user_id
            FROM tasks
            WHERE user_id=%s AND visibility = TRUE
            ORDER BY id ASC
        """, (target_user_id,))
 
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