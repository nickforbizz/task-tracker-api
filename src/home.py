from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import src.models as models
from src.dependencies import get_db 
from .routers import UserController, EventController
app = FastAPI()


app.include_router(UserController.routers, prefix="/users", tags=["Users"])
app.include_router(EventController.routers, prefix="/events", tags=["Events"])

@app.get('/home', tags=['ROOT'])
def root() -> dict:
    return {'msg': 'Welcome '}

@app.get('/events', status_code=status.HTTP_200_OK, tags=['Events'])
async def get_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events