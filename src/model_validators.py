from fastapi import Depends
from pydantic import BaseModel, PositiveInt, validator
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.models import User 

class UserBase(BaseModel):
    username: str
    email: str
    active: bool

class EventBase(BaseModel):
    title: str
    description: str
    fk_user: PositiveInt

