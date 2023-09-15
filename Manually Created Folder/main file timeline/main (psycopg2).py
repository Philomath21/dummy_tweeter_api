from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

new_fastapi_instance = FastAPI()


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


class tweet(BaseModel):
    tweet_content: str
    username: str = "Guest"
    id: int = None 


# GET for basic root url ("/")
@new_fastapi_instance.get("/")
def root():
    return {"message": "Hello World"}


# POST request for /tweets
# Anytime POST request is sent to create tweet, status should be 201
@new_fastapi_instance.post("/tweets", status_code= status.HTTP_201_CREATED)
def new_tweet(post_body : tweet):
    cursor.execute("INSERT INTO tweets (tweet_content, username) VALUES (%s, %s) RETURNING *",
                   (post_body.tweet_content, post_body.username) )
    new_tweet = cursor.fetchone()
    conn.commit()
    return {"tweet": new_tweet}


# GET request for /tweets
@new_fastapi_instance.get("/tweets")
def get_tweets():
    cursor.execute("SELECT * FROM tweets")
    tweets_database = cursor.fetchall()
    return {"tweets": tweets_database}
        

# GET request for specific post /tweets/{id}
# Anytime URL is not found, status should be 404 error
@new_fastapi_instance.get("/tweets/{id}")
def get_tweet_by_id(id: int):
    cursor.execute("SELECT * FROM tweets WHERE id = %s", (str(id),))
    tweet_requested = cursor.fetchone()
    if tweet_requested:
        return {"tweet": tweet_requested}
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id: {str(id)} was not found")
    

# DELETE request for specific post /tweets/{id}
# Anytime post is deleted, status should be 204 & nothing else should be returned
@new_fastapi_instance.delete("/tweets/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_tweet(id:int):
    cursor.execute("DELETE FROM tweets WHERE id = %s RETURNING *", (str(id),))
    tweet_deleted = cursor.fetchone()
    print(tweet_deleted)
    conn.commit()
    if not tweet_deleted:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"Tweet with id:{str(id)} does not exist")


# PUT request to update specific post /tweets/{id}
# Anytime PUT request is sent to update tweet, status should be 201
@new_fastapi_instance.put("/tweets/{id}", status_code= status.HTTP_201_CREATED)
def update_tweet(id: int, put_body: tweet):
    cursor.execute("UPDATE tweets SET username= %s, tweet_content= %s WHERE id= %s RETURNING *", (put_body.username, put_body.tweet_content, str(id)))
    tweet_updated= cursor.fetchone()
    conn.commit()
    if tweet_updated:
         return {"message": f"Tweet has been updated successfully!\n{tweet_updated} "}
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"post with {id} does not exist")









