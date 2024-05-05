from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app import database
from sqlalchemy.orm import Session
from app import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "0ded6267719777b3fcfd099bd63977d4841961c4f201cfb49e28235038cce381"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_tokne(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception

        token_data = schemas.TokenData(id=str(id))

        return token_data
    
    except JWTError:
        raise credential_exception
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not valid credentials", headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_tokne(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user



