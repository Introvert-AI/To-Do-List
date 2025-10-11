from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import datetime
import jwt
import os

SECRET_KEY = "dev-secret-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 1440

#token creation
def create_access_token(data:dict,expires_delta:datetime.timedelta | None=None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE))
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

#Token decodin
def decode_access_token(token:str):
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    except Exception as e:
        print("JWT decode error:",e)
        raise HTTPException(status_code=401,detail=str(e))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
# Middleware / Dependency
security = HTTPBearer()

def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    username = payload.get("username")
    role = payload.get("role")
    if not user_id or not username:
        raise HTTPException(status_code=401,details="Invalid token payload")
    return {"id":int(user_id),"username":username,"role":role}