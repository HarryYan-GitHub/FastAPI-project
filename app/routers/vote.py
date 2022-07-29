from fastapi import APIRouter, Depends, FastAPI, status, HTTPException
from requests import post
from sqlalchemy.orm import Session
from .. import database, models, schemas, oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote, 
    db: Session = Depends(database.get_db), 
    current_user = Depends(oauth2.current_user)
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"User with id {current_user.id} has already voted on post with id {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": f"You have successfully voted on post with id {vote.post_id}"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no vote of user with id {current_user.id} on post with id {vote.post_id}"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": f"successfully deleted your vote on post with id {vote.post_id}"}