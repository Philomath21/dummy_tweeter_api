from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body
import time
from . import models, schemas, utils, oauth2
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import tweet, auth, user
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)
# db: Session = Depends(get_db)     To start a session with database & then close it after usage.

fastapi_instance = FastAPI()


# GET for basic root url: "/"  (200 OK default)
@fastapi_instance.get("/")
def root():
    return {"message": "Hello World"}


fastapi_instance.include_router(tweet.router)
fastapi_instance.include_router(user.router)
fastapi_instance.include_router(auth.router)







