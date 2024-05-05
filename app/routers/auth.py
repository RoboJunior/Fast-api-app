from fastapi import APIRouter, Depends, status , HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Token
from .. import models
from app.utilis import verify_password
from app.oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=Token)
def login(user_cedentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cedentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify_password(user_cedentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type":"bearer"}
