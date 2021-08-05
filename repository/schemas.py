from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    title: str
    description: str
    status: str
    creation_date: datetime
    user_id:int
    class Config():
        orm_mode = True

class ShowTask(BaseModel):
    title: str
    description: str
    status: str
    creation_date: datetime

    class Config():
        orm_mode = True

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: Optional[str] = None
    id: int

class UpdateTask(BaseModel):
    title: str
    description: str
    status: str

    class Config():
        orm_mode = True