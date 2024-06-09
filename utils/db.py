import json
from os import getenv
from typing import List, Union

from dotenv import load_dotenv
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

#from models.articles import ArticleData, ArticleDataMinimum

load_dotenv()

dbclient = AsyncIOMotorClient(getenv("MONGO_URI"))

Database = dbclient.WPQuiz


async def insert_one(collection, data):
    data = json.loads(json.dumps(data, default=str))
    return await Database.get_collection(collection).insert_one(data)


async def find_one(collection, key, value):
    query = {key: {"$eq": value}}
    document = await Database.get_collection(collection).find_one(query)
    document.pop("_id") if document else None
    return document


async def find_many(collection, key, value):
    query = {key: {"$eq": value}}
    documents = []
    async for document in Database.get_collection(collection).find(query):
        document.pop("_id")
        documents.append(document)
    return documents


async def search_db(collection, key, value):
    query = {key: {"$regex": value}}
    documents = []
    async for document in Database.get_collection(collection).find(query):
        document.pop("_id")
        documents.append(document)
    return documents


async def update_one(collection, key, value, data):
    query = {key: {"$eq": value}}
    data = json.loads(json.dumps(data, default=str))
    await Database.get_collection(collection).replace_one(query, data)
    return await find_one(collection, key, value)


async def get_all_documents(collection):
    documents = []
    async for document in Database.get_collection(collection).find():
        document.pop("_id")
        documents.append(document)
    return documents


async def delete_one(collection, key, value):
    query = {key: {"$eq": value}}
    document = await Database.get_collection(collection).delete_one(query)
    return True if document else False

async def get_user(username):
    return await find_one("users", "username", username)

async def login(username, hash) -> bool:
    data = await find_one("users", "username", username)
    if data:
        if data["hash"] == hash:
            return True
        else:
            raise HTTPException(status_code=401, detail="Invalid Password | 잘못된 비밀번호입니다.")
    else:
        raise HTTPException(status_code=404, detail="User Not Found | 사용자를 찾을 수 없습니다.")

async def register(username, hash, name) -> bool:
    if await find_one("users", "username", username):
        raise HTTPException(status_code=409, detail="User Already Exists | 사용자가 이미 존재합니다.")
    else:
        await insert_one("users", {"username": username, "hash": hash, "name":name})
        return True

async def create_quiz(data):
    return await insert_one("quiz", data)

async def search_quiz(query):
    return await search_db("quiz", "title", query)

async def save_session(uuid, quiz):
    return await insert_one("sessions", {"uuid":uuid, "quiz":quiz})