from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
# import psycopg2.extras import RealDictCursor


new_fastapi_instance = FastAPI()

# GET for basic root url ("/")

@new_fastapi_instance.get("/")
def root():
    return {"message": "Hello World"}


###### Trials for Learning Purpose #########################################

# GET for custom url ("/tweet")

@new_fastapi_instance.get("/tweet_trial")
def get_tweet_trial():
    return {"data": "This is one of the tweets"}

# POST (basic; without user data)
@new_fastapi_instance.post("/newtweet_trial1")
def new_tweet_trial1():
    return {"message":"New tweet not created as this function takes no data from the user"}

# POST (with user data- anything allowed as input)
# Add POST body as raw in JSON format
# Example-
# {
#     "content": "Hello Tweeter! This is my first Tweet!",
#     "device": "Soumitra's Windows Laptop"
# }

@new_fastapi_instance.post("/newtweet_trial2")
def new_tweet_trial2(post_body = Body(...)):
    print(post_body)
    return {"new_tweet":f"{post_body}"}


# POST (with user data with constrains)
# Defining class & pydanantic BaseModel to add constrains 

class tweettrial(BaseModel):
    content: str
    device: str
    id: int = None
    user: str = "Guest"   # If data not provided in POST request, it will be "Guest" by default

@new_fastapi_instance.post("/newtweet_trial3")
def new_tweet_trial3(post_body: tweettrial):         # Now the post body will accept the data only if contains 'content' & 'device' data.
    print(post_body)
    # post_body.dict()      Converts into a dictionary
    return {"new_tweet":f"{post_body}"}


###### Main Code ############################################################

### Best Practices

# Use plurals in URL (/tweets not /tweet)
# Use simple, brief & intuitive names (/tweets not /new_tweet)

class tweet(BaseModel):
    content: str
    device: str
    id: int = None
    user: str = "Guest" 

# Using id variable to store posts. In original projects, Database will be used
tweets_database = []     # Store posts in dictionary format

# Function to assign id to the tweet & append it to the database list
def append_to_database_with_id(post_body):
    tweet_as_dict = post_body.dict()
    tweet_as_dict['id'] = randrange(0, 10000000)
    tweets_database.append(tweet_as_dict)
    return tweet_as_dict['id']


# POST request for /tweets
# Anytime POST request is sent to create tweet, status should be 201
@new_fastapi_instance.post("/tweets", status_code= status.HTTP_201_CREATED)
def new_tweet(post_body : tweet):
    append_to_database_with_id(post_body)
    print (tweets_database[-1])
    return {"tweet": f"{tweets_database[-1]}"}


# GET request for /tweets
@new_fastapi_instance.get("/tweets")
def get_tweets():
    return {"tweets": f"{tweets_database}"}


# Find tweet in database list using id
# This function will be useful in many functions below
def find_tweet_by_id(id: int):
    for tweet_as_dict in tweets_database:
        if tweet_as_dict["id"] == id:
            return tweet_as_dict
        

# GET request for specific post /tweets/{id}
# Anytime URL is not found, status should be 404 error
@new_fastapi_instance.get("/tweets/{id}")
def get_tweet_by_id(id: int):  # ,response: Response
    if find_tweet_by_id(id):
        return { "tweet" : find_tweet_by_id(id)}
    else:
        # Dirtier way commented out
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} was not found"}
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"post with {id} was not found")
    

# DELETE request for specific post /tweets/{id}
# Anytime post is deleted, status should be 204 & nothing else should be returned
@new_fastapi_instance.delete("/tweets/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_tweet(id:int):
    if find_tweet_by_id(id):
        tweets_database.remove(find_tweet_by_id(id))
        # return Response(status_code= status.HTTP_204_NO_CONTENT)
        return None
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"post with {id} does not exist")


# PUT request to update specific post /tweets/{id}
# Anytime PUT request is sent to update tweet, status should be 201
@new_fastapi_instance.put("/tweets/{id}", status_code= status.HTTP_201_CREATED)
def update_tweet(id: int, put_body: tweet):
    if find_tweet_by_id(id):
        tweet_as_dict = put_body.dict()
        tweet_as_dict["id"]= id
        index = tweets_database.index(find_tweet_by_id(id))
        tweets_database[index]= tweet_as_dict
        return {"tweet": tweet_as_dict}
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"post with {id} does not exist")


### Connect to PostGreSQL using psycopg2

try:
	# Connect to postgres DB
	conn = psycopg2.connect(host= 'localhost', database= 'API project FastAPI', user= 'postgres', password= 'Trim0.5')

	# Open a cursor to perform database operations
	cur = conn.cursor()
	print("Database connected successfully")

except Exception as error:
	print("Connection to database failed.")
	print(f"Error: {error}")



