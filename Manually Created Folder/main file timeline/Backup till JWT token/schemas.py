from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# 'schema'/pydantic model: used to control request (POST or PUT) & response body
class Tweet_base(BaseModel):       
    tweet_content: str
    username: str = "Guest"

# POST, PUT request schemas model for Tweet
class Tweet_create(Tweet_base):
    pass

# POST, GET, PUT response schemas model for Tweet
class Tweet_response(Tweet_base):
    created_at : datetime
    class Config:
        orm_mode= True

######################################################

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

# Request schema model for Token
class Token(BaseModel):
    access_token : str
    token_type : str

# Request schema model for payload data passed while creating access token
class Access_token_Payload_data(BaseModel):
    username : Optional[EmailStr] = None        # We are using email as username here