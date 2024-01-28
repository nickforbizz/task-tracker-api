from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union

import src.models as models
from src.db import engine, SessionLocal
from src.model_validators import UserBase
from src.dependencies import get_db 

routers = APIRouter()
models.Base.metadata.create_all(bind=engine)




@routers.get('/users', status_code=status.HTTP_200_OK, tags=['Users'])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@routers.get('/user/{user_id}', status_code=status.HTTP_200_OK ,tags=['Users'])
async def get_user(user_id: int, q: Union[str, None] = None, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@routers.post('/user', status_code=status.HTTP_201_CREATED ,tags=['Users'])
async def create_user(user: UserBase, db: Session=Depends(get_db)):
    user = models.User(**user.model_dump())
    db.add(user)
    db.commit()
    return user

#function to update user
@routers.put('/user/{user_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Users'])
async def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)

    if user_query.first() is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_query.update(user.model_dump(), synchronize_session=False)
    db.commit()

    return user_query.first()

@routers.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    # Return None with status_code=204 (No Content)
    return None  

async def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()  
    return user