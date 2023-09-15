from random import randrange
from typing import Optional
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

# db: Session = Depends(get_db)
@new_fastapi_instance.get("/trial")
def test_funct(db: Session = Depends(get_db)):
     tweets= db.query(models.Tweet).all()
     return {"status": tweets}


### Connect to PostGreSQL using psycopg2
try:
	# Connect to postgres DB
	conn = psycopg2.connect(host= 'localhost', database= 'API project FastAPI', user= 'postgres', password= 'Trim0.5', cursor_factory=RealDictCursor )

	# Open a cursor to perform database operations
	cursor = conn.cursor()
	print("Database connected successfully")

except Exception as error:
	print("Connection to database failed.")
	print(f"Error: {error}")
# These print statements inform the developer about the status of database connection, in the terminal.


# GET for basic root url ("/")
@new_fastapi_instance.get("/")
def root():
    return {"message": "Hello World"}


# POST request for /tweets
# Anytime POST request is sent to create tweet, status should be 201
# psycopg2 code commented out below
@new_fastapi_instance.post("/tweets", status_code= status.HTTP_201_CREATED)
def new_tweet(post_body : schemas.Tweet_create, db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO tweets (tweet_content, username) VALUES (%s, %s) RETURNING *",
    #               (post_body.tweet_content, post_body.username) )
    # new_tweet = cursor.fetchone()
    # conn.commit()
    new_tweet= models.Tweet(**post_body.dict())
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)     # Replaces RETURNING *
    # POST request is successfull without refresh, but to return the contents of it, refresh must be used.
    return {"tweet": new_tweet}


# GET request for /tweets
@new_fastapi_instance.get("/tweets")
def get_tweets(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM tweets")
    # tweets_database = cursor.fetchall()   
    tweets_database = db.query(models.Tweet).all()    # .all() stands for cursor.fetchall()
    return {"tweets": tweets_database}
        

# GET request for specific post /tweets/{id}
# Anytime URL is not found, status should be 404 error
@new_fastapi_instance.get("/tweets/{id}")
def get_tweet_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM tweets WHERE id = %s", (str(id),))
    # tweet_requested = cursor.fetchone()
    tweet_requested= db.query(models.Tweet).filter(models.Tweet.id== id).first()   
    # Filter stands for WHERE, first() stands for cursor.fetchone()
    if tweet_requested:
        return {"tweet": tweet_requested}
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id: {str(id)} was not found")
    

# DELETE request for specific post /tweets/{id}
# Anytime post is deleted, status should be 204 & nothing else should be returned except Response(status_code= status.HTTP_204_NO_CONTENT)
@new_fastapi_instance.delete("/tweets/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_tweet(id:int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM tweets WHERE id = %s RETURNING *", (str(id),))
    # tweet_deleted = cursor.fetchone()
    # print(tweet_deleted)
    # conn.commit()
    tweet_requested= db.query(models.Tweet).filter(models.Tweet.id== id)

    if tweet_requested.first():
        tweet_requested.delete(synchronize_session= False)
        db.commit()
        # return Response(status_code= status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id:{str(id)} does not exist")


# PUT request to update specific post /tweets/{id}
# Anytime PUT request is sent to update tweet, status should be 201
@new_fastapi_instance.put("/tweets/{id}", status_code= status.HTTP_201_CREATED)
def update_tweet(id: int, put_body: schemas.Tweet_update, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE tweets SET username= %s, tweet_content= %s WHERE id= %s RETURNING *", (put_body.username, put_body.tweet_content, str(id)))
    # tweet_updated= cursor.fetchone()
    # conn.commit()
    tweet_query = db.query(models.Tweet).filter(models.Tweet.id== id)
    tweet_requested= tweet_query.first()

    if tweet_requested:
         tweet_query.update(put_body.dict(), synchronize_session=False)
         db.commit()
         return {"message": "Tweet has been updated successfully!"}
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"post with {id} does not exist")









