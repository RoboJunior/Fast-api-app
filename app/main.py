from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import  RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .schemas import PostCreate_and_Update,PostRespose


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres', password='jeya2001', cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print("Database Connected Successfully ...")
        break
    except Exception as e:
        print(f"Error connecting to Database : {e}")
        time.sleep(2)

@app.get("/")
def root():
    return {"hello": "world"}

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    # curr.execute("""SELECT * FROM posts;""")
    # posts = curr.fetchall()
    # print(posts)
    # Standard Sql operation
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=PostRespose)
def create_post(post: PostCreate_and_Update, db: Session = Depends(get_db)):
    # curr.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = curr.fetchone()
    # conn.commit()
    # Standard Sql operation
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # curr.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    # post = curr.fetchone()
    # conn.commit()
    # Standard Sql operation
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    return post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # curr.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
    # post = curr.fetchone()
    # conn.commit()
    # Standard Sql operation
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found.")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=PostRespose)
def update_post(id: int, post: PostCreate_and_Update, db: Session = Depends(get_db)):
    # curr.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s returning *""",(post.title, post.content, post.published, str(id)))
    # updated_post = curr.fetchone()
    # conn.commit()
    # Standard Sql operation
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()
    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found.")
    
    post_query.update(post.dict(),synchronize_session=False)

    db.commit()
    
    return post_query.first()

