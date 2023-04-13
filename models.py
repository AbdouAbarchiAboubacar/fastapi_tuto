from tortoise import fields, models
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from pydantic import BaseModel, Field
from typing import List, Optional, Generic, TypeVar


class Todo(models.Model):
    id = fields.IntField(pk=True, index=True)
    title = fields.CharField(max_length=250)
    description = fields.CharField(max_length=250)

    class PydanticMeta:
        pass


class TodoBaseModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


Todo_Pydantic = pydantic_model_creator(Todo, name="Todo")
TodoIn_Pydantic = pydantic_model_creator(
    Todo, name="TodoIn", exclude_readonly=True)
