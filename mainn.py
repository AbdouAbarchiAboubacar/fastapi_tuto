from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from typing import Optional, List
from models import Todo_Pydantic, TodoIn_Pydantic, Todo, TodoBaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise


class Message(BaseModel):
    message: str


app = FastAPI()


@app.post("/todo/", response_model=Todo_Pydantic)
async def create(todo: TodoBaseModel):
    obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(obj)


@app.get("/todo/{id}", response_model=Todo_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_todo(id: int):
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))


@app.put("/todo/{id}", response_model=Todo_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_todo(id: int, todo: TodoBaseModel):
    await Todo.filter(id=id).update(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))


@app.delete("/todo/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_todo(id: int):
    delete_obj = await Todo.filter(id=id)
    if not delete_obj:
        raise HTTPException(status_code=404, detail="Not Found")
    return Message(message="Successfully delete todo")


register_tortoise(app, db_url="sqlite://store.db",
                  modules={'models': ['models']}, generate_schemas=True, add_exception_handlers=True)
