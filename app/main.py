from fastapi import FastAPI
from . import models
from .database import engine
from .routers import tweet, auth, user, like
from.config import settings


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
fastapi_instance.include_router(like.router)







