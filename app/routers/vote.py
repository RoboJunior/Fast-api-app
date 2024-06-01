from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. schemas import Vote
from app.database import get_db
from app import oauth2
from .. import models
from sqlalchemy.orm import Session



router = APIRouter(prefix='/vote',tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
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
        
        
