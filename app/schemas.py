from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class Post(BaseModel):
    title: str
    content: str
    published : bool = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True    

class PostCreate_and_Update(PostBase):
    pass

class PostRespose(PostBase):
    id : int
    created_at: datetime
    user_id: int
    user: UserResponse
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: PostRespose
    votes: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None


class Vote(BaseModel):
    post_id: int
    like: Literal[0,1]


