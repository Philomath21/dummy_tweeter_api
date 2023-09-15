from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/tweets/{tweet_id}/like",
    tags= ["Likes"]
    )


# def get_tweet_by_id(tweet_id: int,
#                     db: Session = Depends(get_db)):
#     tweet_requested= db.query(models.Tweet).filter(models.Tweet.id== tweet_id).first()   
#     if tweet_requested:
#         return tweet_requested
#     else:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
#                         detail= f"Tweet with id: {str(tweet_id)} was not found")


# # GET request for specific tweet likes  /{tweet_id}/like  (200 OK default or 404 NOT FOUND)
# @router.get("/")
# def get_tweet_like(tweet_id : int,
#                  db: Session = Depends(get_db)):
#         get_tweet_by_id(tweet_id= tweet_id)      # Checking if tweet exists
#         likes_list= db.query(models.Like).filter(models.Like.tweet_id == tweet_id).all()
#         return likes_list
    

# GET request for specific tweet likes  
# /{tweet_id}/like  (200 OK default or 404 NOT FOUND)
@router.get("/")
def get_tweet_like(tweet_id : int,
                 db: Session = Depends(get_db)):
    tweet_requested= db.query(models.Tweet).filter(models.Tweet.id== tweet_id).first()   
    if tweet_requested:      # Checking if tweet exists
        likes_list= db.query(models.Like).filter(models.Like.tweet_id == tweet_id).all()
        return likes_list
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id: {str(tweet_id)} was not found")


# POST request. Like specific post by specific user: 
# /{tweet_id}/like  (201 CREATED or 409 CONFLICT)
@router.post("/",
             status_code= status.HTTP_201_CREATED)
def like_tweet(tweet_id : int,
               db: Session = Depends(get_db),
               user_logged_in = Depends(oauth2.get_current_user)):
    tweet_requested= db.query(models.Tweet).filter(models.Tweet.id== tweet_id).first()   
    if tweet_requested:     # Checking if tweet exists
        like_tweet_entry = models.Like(tweet_id = tweet_id, user_id = user_logged_in.id)
        try:
            db.add(like_tweet_entry)
            db.commit()
            return {"message" : "Liked!"}
        except:   # If duplicate like entry is being created, raise 409 CONFLICT
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                                detail= "You have already liked this post")
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id: {str(tweet_id)} was not found")


# DELETE request. Unlike specific post by specific user:  
# /{tweet_id}/like  (204 NO CONTENT or 404 NOT FOUND)
@router.delete("/",
               status_code= status.HTTP_204_NO_CONTENT)
def unlike_tweet(tweet_id : int,
                 db: Session = Depends(get_db),
                 user_logged_in = Depends(oauth2.get_current_user)):
    tweet_requested= db.query(models.Tweet).filter(models.Tweet.id== tweet_id).first()   
    if tweet_requested:      # Checking if tweet exists
        like_query= db.query(models.Like).filter(
            models.Like.tweet_id == tweet_id, models.Like.user_id == user_logged_in.id)
        like_requested = like_query.first()
        if like_requested:    # Checking if post is liked or not
            like_query.delete(synchronize_session= False)
            db.commit()
        else:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= "You have not liked this tweet yet!")
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id: {str(tweet_id)} was not found")
    