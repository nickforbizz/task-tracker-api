from sqlalchemy.orm import Session
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from src.db import SessionLocal

# Dependency to get the database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# OAuth2 Setup
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://accounts.google.com/o/oauth2/token",
    refreshUrl="https://accounts.google.com/o/oauth2/token",
    scopes={"openid": "OpenID connect scope"}
)