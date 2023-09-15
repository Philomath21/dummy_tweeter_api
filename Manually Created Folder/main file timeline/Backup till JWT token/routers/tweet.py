from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2 # .. implies 2 folders outside
from ..database import get_db
from typing import List

router = APIRouter(
    prefix= "/tweets",
    tags= ["Tweets"]
    )



# POST request: /  (201 CREATED)
@router.post("/",
             response_model= schemas.Tweet_response,
             status_code= status.HTTP_201_CREATED)
def new_tweet(post_body : schemas.Tweet_create,
              db: Session = Depends(get_db),
              payload_data = Depends(oauth2.get_current_user)):
    new_tweet= models.Tweet(**post_body.dict())
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)      # POST request is successfull without refresh, but to return the contents of it, refresh must be used.
    return new_tweet


# GET request: /  (200 OK default)
@router.get("/",
            response_model= List[schemas.Tweet_response])
def get_(db: Session = Depends(get_db)):  
    _database = db.query(models.Tweet).all()    # .all() stands for cursor.fetchall()
    return _database
        

# GET request for specific tweet: //{id}  (200 OK default or 404 NOT FOUND)
@router.get("/{id}",
            response_model= schemas.Tweet_response)
def get_tweet_by_id(id: int,
                    db: Session = Depends(get_db)):
    tweet_requested= db.query(models.Tweet).filter(models.Tweet.id== id).first()   
    if tweet_requested:
        return tweet_requested
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id: {str(id)} was not found")
    

# DELETE request for specific tweet: //{id}  (204 NO CONTENT or 404 NOT FOUND)
# return is not permitted for delete
@router.delete("/{id}",
               status_code= status.HTTP_204_NO_CONTENT)
def delete_tweet(id:int,
                 db: Session = Depends(get_db)):
    tweet_requested= db.query(models.Tweet).filter(models.Tweet.id== id)
    if tweet_requested.first():
        tweet_requested.delete(synchronize_session= False)
        db.commit()
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id:{str(id)} does not exist")


# PUT request to update specific tweet: //{id}  (201 CREATED)
@router.put("/{id}",
            response_model= schemas.Tweet_response,
            status_code= status.HTTP_201_CREATED)
def update_tweet(id: int,
                 put_body: schemas.Tweet_create,
                 db: Session = Depends(get_db)):
    tweet_query = db.query(models.Tweet).filter(models.Tweet.id== id)
    tweet_requested= tweet_query.first()
    if tweet_requested:
         tweet_query.update(put_body.dict(), synchronize_session=False)
         db.commit()
         db.refresh(tweet_requested)
         return tweet_requested
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"post with {id} does not exist")