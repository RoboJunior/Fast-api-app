from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db, engine
from .. import models
from app.schemas import PostCreate_and_Update, PostRespose
from app.utilis import hash_password
from app import oauth2



router = APIRouter(prefix="/posts",tags=["Posts"])




@router.get("/")
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("""SELECT * FROM posts;""")
    # posts = curr.fetchall()
    # print(posts)
    # Standard Sql operation
    posts = db.query(models.Post).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=PostRespose)
def create_post(post: PostCreate_and_Update, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = curr.fetchone()
    # conn.commit()
    # Standard Sql operation
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=PostRespose)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    # post = curr.fetchone()
    # conn.commit()
    # Standard Sql operation
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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

@router.put("/{id}", response_model=PostRespose)
def update_post(id: int, post: PostCreate_and_Update, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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