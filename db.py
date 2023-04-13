from typing import List
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import databases
import sqlalchemy

DATABASE_URL = 'sqlite:///./store.db'

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

register = sqlalchemy.Table("register", metadata, sqlalchemy.Column(
    "id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
    "title", sqlalchemy.String(500)),
    sqlalchemy.Column(
    "due_date", sqlalchemy.DateTime())
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={
                                  "check_same_thread": False})

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def connect():
    await database.connect()


@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()


class Register(BaseModel):
    id: int
    title: str
    due_date: datetime


class registerIn(BaseModel):
    title: str = Field(...)


@app.post("/register/", response_model=Register)
async def create(r: registerIn = Depends()):
    query = register.insert().values(
        title=r.title,
        due_date=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}  # type:ignore


@app.get("/register/{id}", response_model=Register)
async def get_one(id: int):
    query = register.select().where(register.c.id == id)
    user = await database.fetch_one(query)
    return {**user} # type:ignore


@app.get("/register/", response_model=List[Register])
async def get_all():
    query = register.select()
    all_get = await database.fetch_all(query)
    return all_get


@app.put("/register/{id}", response_model=Register)
async def update(id: int, r: registerIn = Depends()):
    query = register.update().where(register.c.id == id).values(
        title=r.title, due_date=datetime.utcnow())
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row} # type:ignore


@app.delete("/register/{id}")
async def delete(id: int):
    query = register.delete().where(register.c.id == id)
    return await database.execute(query)
