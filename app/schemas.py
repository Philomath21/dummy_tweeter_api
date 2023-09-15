from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime



# BaseModel for creating User
class User_base(BaseModel):
    email : EmailStr

# POST, PUT request schemas model for User
class User_request (User_base):
    password : str

# GET, POST, PUT response schemas model for User
class User_response(User_base):
    class Config:
        orm_mode = True

#######################################################
# 'schema'/pydantic model: used to control request (POST or PUT) & response body
class Tweet_base(BaseModel):       
    tweet_content: str
    
# POST, PUT request schemas model for Tweet
class Tweet_create(Tweet_base):
    pass

# schema for reference in response schema model
class Tweet_response(Tweet_base):
    id : int
    created_at : datetime
    user_id : int
    user_details : User_response
    class Config:
        orm_mode= True

# POST, GET, PUT response schemas model for Tweet, with likes count
class Tweet_response_with_likes(BaseModel):
    Tweet : Tweet_response
    likes : int
    class Config:
        orm_mode= True


######################################################

# Response schema model for Token
class Token(BaseModel):
    access_token : str
    token_type : str

# Request schema model for payload data passed while creating access token
class Access_token_Payload_data(BaseModel):
    username : Optional[EmailStr] = None        # We are using email as username here
