from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published : bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate_and_Update(PostBase):
    pass

class PostRespose(BaseModel):
    title: str
    content: str
    

