from database import global_connection, init_data, init_log
from auth import create_access_token, get_current_user
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import bcrypt

init_log()
init_data()
app = FastAPI()

# Models
class TaskModel(BaseModel):
    task: str
    status: str

class RegisterModel(BaseModel):
    username: str
    password: str
    age: int

class LoginModel(BaseModel):
    username: str
    password: str

# --- Akun ---
@app.post("/todolist/account/register")
def register(data: RegisterModel):
    hashed_pw = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    with global_connection() as conn:
        cur = conn.cursor()
        try:
            print("DEBUG INSERT:", data.username, hashed_pw, data.age)
            cur.execute("INSERT INTO account_data (username, pw_hash, age) VALUES (?,?,?)",
                        (data.username, hashed_pw, data.age))
            conn.commit()
            user_id = cur.lastrowid
            print("DEBUG user_id:", user_id)
            return {"message": "berhasil", "user_id": user_id}
        except Exception as e:
            print("DEBUG register error:", e)
            if "UNIQUE constraint failed" in str(e):
                raise HTTPException(status_code=400, detail="Username already exists")
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/todolist/account/login")
def login_account(data: LoginModel):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, pw_hash FROM account_data WHERE username = ?", (data.username,))
        user = cur.fetchone()
        print("DEBUG user:", user)
    if not user or not bcrypt.checkpw(data.password.encode("utf-8"), user["pw_hash"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": str(user["id"]), "username": user["username"]})
    return {"access_token": token, "token_type": "bearer", "user_id": user["id"]}

@app.get("/todolist/account/info")
def account_info(current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, age FROM account_data WHERE id=?", (current_user["id"],))
        user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user["username"], "age": user["age"]}

# --- Tasks ---
@app.post("/todolist/addtask")
def add_task(data: TaskModel, current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO task_data (task, status, user_id) VALUES (?,?,?)",
                    (data.task, data.status, current_user["id"]))
        conn.commit()

@app.get("/todolist/getalltask")
def get_all_tasks(current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT task_id, task, status FROM task_data WHERE user_id=?", (current_user["id"],))
        rows = cur.fetchall()
    tasks = [{"task_id": row[0], "task": row[1], "status": row[2]} for row in rows]
    return {"task": tasks}


@app.put("/todolist/updatenametask/{task_id}")
def update_task(nama_baru:str, task_id:int, current_user:dict =Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE task_data SET task=? WHERE task_id=? AND user_id=?", 
                       (nama_baru, task_id, current_user["id"]))
        conn.commit()
        if cur.rowcount > 0:
            return {"success":True,"message":"Tugas Berhasil Diubah"}
        else:
            return {"succes":False,"message":"Tugas tidak ditemukan"}
        
@app.put("/todolist/updatestatustask/{task_id}")
def status_change(task_id:int,current_user:dict=Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT status FROM task_data WHERE task_id=? AND user_id=?", (task_id,current_user["id"]))
        row = cur.fetchone()

        if not row:
            return {"success": False, "message": "Tugas tidak ditemukan"}

        current_status = row[0]  # cukup sekali fetchone

        new_status = "Selesai" if current_status != "Selesai" else "Belum Selesai"

        cur.execute(
            "UPDATE task_data SET status=? WHERE task_id=? AND user_id=?",
            (new_status, task_id, current_user["id"])
        )
        conn.commit()

        if cur.rowcount > 0:
            return {"success": True, "message": f"Status task berhasil diubah ke {new_status}"}
        else:
            return {"success": False, "message": "Tugas tidak ditemukan"}
        

@app.delete("/todolist/deletetask/{task_id}")
def delete_task(task_id:int, current_user:dict=Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM task_data WHERE task_id=? AND user_id=?", (task_id, current_user["id"]))
        conn.commit()
    if cur.rowcount > 0:
        return {"success": True, "message": "Tugas berhasil dihapus"}
    else:
        return {"success": False, "message": "Tugas tidak ditemukan"}

