from core.database import global_connection
from core.auth import create_access_token, get_current_user
from fastapi import APIRouter, Depends
from pydantic import BaseModel
import bcrypt

router = APIRouter(
    prefix="/account",
    tags=["account"]
)

class RegisterModel(BaseModel):
    username: str
    password: str
    age: int

class LoginModel(BaseModel):
    username: str
    password: str
    
# --- Akun ---
@router.post("/register")
def register(data: RegisterModel):
    hashed_pw = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    with global_connection() as conn:
        cur = conn.cursor()
        print("DEBUG INSERT:", data.username, hashed_pw, data.age)
        cur.execute(
            "INSERT INTO users (username, hash_pw, age) VALUES (%s,%s,%s) RETURNING id",
            (data.username, hashed_pw, data.age)
        )
        user_id = cur.fetchone()  
        conn.commit()
        print("DEBUG user_id:", user_id)
        return {"message": "berhasil", "user_id": user_id}


@router.post("/login")
def login_account(data: LoginModel):
    with global_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, hash_pw, role FROM users WHERE username = %s",
            (data.username,)
        )
        user = cur.fetchone()
        print("DEBUG user:", user)
        
    if not user or not bcrypt.checkpw(data.password.encode("utf-8"), user["hash_pw"].encode("utf-8")):
        return {"error": "Invalid username or password"}
    
    token = create_access_token({"sub": str(user["id"]), "username": user["username"], "role": user["role"]})
    
    return {"access_token": token, "token_type": "bearer", "user_id": user["id"], "role": user["role"]}

#API untuk sidebar
@router.get("/my_info/{username}")
def personal_info(username:str , current_user: dict = Depends(get_current_user)):
    with global_connection() as conn:
        cur = conn.cursor()
        
        cur.execute(
            "SELECT username, age FROM users WHERE username=%s",
            (username,)
        )
        user = cur.fetchone()
        
    if not user:
        return {"error": "User not found"}
    
    return {"username": user["username"], "age": user["age"]}


@router.get("/info/all")
def public_info(current_user:dict=Depends(get_current_user)):
    with global_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT username FROM users")
            row = [row["username"] for row in cur.fetchall()]
            return {"all_account":row}