from fastapi import Depends
from pydantic import BaseModel, PositiveInt, validator
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.models import User 

class UserBase(BaseModel):
    username: str
    active: bool

class EventBase(BaseModel):
    name: str
    description: str
    fk_user: PositiveInt

#     @validator("fk_user")
#     def validate_fk_user_exists(cls, value, values):
#         db = values.get("db")  # Assuming you pass the database session to the Pydantic model
#         if not check_user_exists(value):
#             raise ValueError("User with ID does not exist")
#         return value
    
# def check_user_exists(user_id: int) -> bool:
#     db: Session = Depends(get_db)
#     user = db.query(User).filter(User.id == user_id).first()
#     return user is not None