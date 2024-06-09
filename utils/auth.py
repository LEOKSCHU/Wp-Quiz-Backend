from fastapi import HTTPException
from utils import db
from dotenv import load_dotenv
import hashlib
import os
import jwt

load_dotenv()

def hash_passsword(password):
    return hashlib.sha256((password+os.environ.get("SALT")).encode()).hexdigest()

async def generate_token(username, password):
    if await db.login(username, hash_passsword(password)):
        return jwt.encode({"username": username, "iss":"LKQUIZ"}, os.environ.get("JWT_SECRET"), algorithm="HS256")
    else:
        raise HTTPException(status_code=401, detail="Invalid Credentials | 올바르지 않은 인증 정보입니다.")

async def register_account(username, password, name):
    return await db.register(username, hash_passsword(password), name)

async def verify_token(token: str):
    token = token.replace("Bearer ", "")
    try:
        return jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid Credentials | 올바르지 않은 인증 정보입니다.")