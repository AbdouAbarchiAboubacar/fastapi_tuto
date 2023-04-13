# from fastapi import FastAPI, HTTPException, Form
# from pydantic import BaseModel
# from typing import Optional, List

# # 1. Define an API object
# app = FastAPI()


# class Todo(BaseModel):
#     name: str
#     description: str
#     due_date: str


# store_todo = []


# @app.get("/todos/", response_model=List[Todo])
# async def get_all_todos():
#     return store_todo


# @app.get("/todo/{id}")
# async def get_todo(id: int):
#     try:
#         return store_todo[id]
#     except:
#         raise HTTPException(status_code=404, detail="Todo not found")


# @app.post("/todo/")
# async def create_todo(todo: Todo):
#     store_todo.append(todo)
#     return todo


# @app.put("/todo/{id}")
# async def update_todo(id: int, new_todo: Todo):
#     try:
#         store_todo[id] = new_todo
#         return HTTPException(status_code=200, detail="Todo Updated")
#     except:
#         raise HTTPException(status_code=404, detail="Todo not found")


# @app.delete("/todo/{id}")
# async def delete_todo(id: int):
#     try:
#         store_todo.pop(id)
#         return HTTPException(status_code=200, detail="Todo Deleted")
#     except:
#         raise HTTPException(status_code=404, detail="Todo not found")


# @app.post("/login/")
# async def login(username: str = Form(...), password: str = Form(...)):
#     return {"username": username}
