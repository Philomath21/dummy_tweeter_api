from random import randrange
from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

new_fastapi_instance = FastAPI()


# GET for basic root url: "/"  (200 OK default)
@new_fastapi_instance.get("/")
def root():
    return {"message": "Hello World"}


# POST request: /tweets  (201 CREATED)
@new_fastapi_instance.post("/tweets",
                           response_model= schemas.Tweet_response,
                           status_code= status.HTTP_201_CREATED)
def new_tweet(post_body : schemas.Tweet_create,
              db: Session = Depends(get_db)):
    new_tweet= models.Tweet(**post_body.dict())
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)      # POST request is successfull without refresh, but to return the contents of it, refresh must be used.
    return new_tweet


# GET request: /tweets  (200 OK default)
@new_fastapi_instance.get("/tweets",
                          response_model= List[schemas.Tweet_response])
def get_tweets(db: Session = Depends(get_db)):  
    tweets_database = db.query(models.Tweet).all()    # .all() stands for cursor.fetchall()
    return tweets_database
        

# GET request for specific tweet: /tweets/{id}  (200 OK default or 404 NOT FOUND)
@new_fastapi_instance.get("/tweets/{id}",
                          response_model= schemas.Tweet_response)
def get_tweet_by_id(id: int,
                    db: Session = Depends(get_db)):
    tweet_requested= db.query(models.Tweet).filter(models.Tweet.id== id).first()   
    if tweet_requested:
        return tweet_requested
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id: {str(id)} was not found")
    

# DELETE request for specific tweet: /tweets/{id}  (204 NO CONTENT or 404 NOT FOUND)
# return is not permitted for delete
@new_fastapi_instance.delete("/tweets/{id}",
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


# PUT request to update specific tweet: /tweets/{id}  (201 CREATED)
@new_fastapi_instance.put("/tweets/{id}",
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









