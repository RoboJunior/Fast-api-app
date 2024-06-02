from fastapi import Response, status, HTTPException, Depends, APIRouter, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from .. import models
from app.schemas import PostCreate_and_Update, PostRespose, PostOut
from app import oauth2
from typing import List, Optional, Annotated
from sqlalchemy import func
import base64


router = APIRouter(prefix="/posts",tags=["Posts"])


@router.get("/", response_model=List[PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    # curr.execute("""SELECT * FROM posts;""")
    # posts = curr.fetchall()
    # print(posts)
    # Standard Sql operation
    results = (
    db.query(
        models.Post,
        func.count(models.Post.id).label("votes"),
        models.Comment.id.label("comment_id"),
        models.Comment.content.label("comment"),
        models.User.email.label("commented_by")
    )
    .outerjoin(models.Votes, models.Post.id == models.Votes.post_id)
    .outerjoin(models.Comment, models.Post.id == models.Comment.post_id)
    .outerjoin(models.User, models.Comment.user_id == models.User.id)
    .filter(models.Post.title.contains(search))
    .group_by(models.Post.id, models.Comment.id, models.User.email).all())
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostRespose)
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    published: bool = Form(...),
    file: Annotated[UploadFile, File()] = None,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    try:
        post_data = PostCreate_and_Update(title=title, content=content, published=published)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {e}")
    print(file.filename)
    if file:
        content = await file.read()
        base64_bytes = base64.b64encode(content)
        base64_string = base64_bytes.decode('utf-8')
        new_post = models.Post(
            user_id=current_user.id,
            **post_data.dict(),
            image=base64_string
        )
    else:
        new_post = models.Post(
            user_id=current_user.id,
            **post_data.dict(),
            image="No image uploaded"
            )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    # post = curr.fetchone()
    # conn.commit()
    # Standard Sql operation
    post = (
    db.query(
        models.Post,
        func.count(models.Post.id).label("votes"),
        models.Comment.content.label("comment"),
        models.User.email.label("commented_by"),
        models.Comment.created_at.label("created_at")
    )
    .outerjoin(models.Votes, models.Post.id == models.Votes.post_id)
    .outerjoin(models.Comment, models.Post.id == models.Comment.post_id)
    .outerjoin(models.User, models.Comment.user_id == models.User.id)).group_by(models.Post.id, models.Comment.id, models.User.email).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curr.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
    # post = curr.fetchone()
    # conn.commit()
    # Standard Sql operation
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found.")
    if current_user.id != post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform with requested action")
    
    post_query.delete(synchronize_session=False)
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
    if current_user.id != update_post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform with requested action")

    post_query.update(post.dict(),synchronize_session=False)

    db.commit()
    
    return post_query.first()