from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import requests, os
import src.models as models
from src.model_validators import UserBase
from src.dependencies import get_db 
from src.routers.UserController import get_user_by_email, create_user
from .routers import UserController, EventController
app = FastAPI()
 


app.include_router(UserController.routers, prefix="/users", tags=["Users"])
app.include_router(EventController.routers, prefix="/events", tags=["Events"])

@app.get("/login")
async def login_via_google():   
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = "http://localhost:8000/auth"
    return {
        "url": f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=openid%20email&access_type=offline"
    }

@app.get("/auth")
async def authenticate_user(code: str, db: Session = Depends(get_db)):
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uri = "http://localhost:8000/auth"
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    token_r = requests.post(token_url, data=token_data)
    token = token_r.json()
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    user_info_r = requests.get(user_info_url, headers={"Authorization": f"Bearer {token['access_token']}"})
    user_info = user_info_r.json()

    # Check if user exists in DB, if not, add them
    user = await get_user_by_email(db, email=user_info["email"])
    if not user:
        user_data = {
            'username': user_info["email"].split("@")[0],
            'email': user_info["email"],
            'active': True  
        }
        user = await create_user(user=UserBase(**user_data),db=db)
    return {"user": user_data}


@app.get('/home', tags=['ROOT'])
def root() -> dict:
    return {'msg': 'Welcome '}

@app.get('/events', status_code=status.HTTP_200_OK, tags=['Events'])
async def get_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events