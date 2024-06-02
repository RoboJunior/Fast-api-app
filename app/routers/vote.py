from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. schemas import Vote, Comment
from app.database import get_db
from app import oauth2
from .. import models
from sqlalchemy.orm import Session

vote_router = APIRouter(prefix='/vote',tags=["Vote"])
comment_router = APIRouter(prefix='/comment', tags=["Comment"])

@vote_router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.like == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You have already liked this post")
        new_like = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "You have liked this post."}
    elif vote.like == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} was not found.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "You have unliked the post"}

@comment_router.post("/", status_code=status.HTTP_201_CREATED)
def comment(comment: Comment, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not comment.comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment cannot be empty")
    
    new_comment = models.Comment(post_id=comment.post_id, user_id=current_user.id, content=comment.comment)
    db.add(new_comment)
    db.commit()
    
    return {"message": "You have commented on this post."}

@comment_router.delete("/{comment_id}", status_code=status.HTTP_201_CREATED)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.user_id == current_user.id)
    found_comment = comment_query.first()
    
    if not found_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found or you're not authorized to delete this comment")
    
    comment_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": "Comment deleted successfully"}
        
