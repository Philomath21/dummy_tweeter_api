from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils  # .. implies 2 folders outside
from ..database import get_db

router = APIRouter(
    prefix= "/users",
    tags= ["Users"]
    )

# POST request to create new user: /users  (201 CREATED)
@router.post("/",
             response_model= schemas.User_response,
             status_code= status.HTTP_201_CREATED)
def create_user(post_body: schemas.User_request,
                db: Session = Depends(get_db)):
    # Hashing the password recieved in the request
    post_body.password = utils.get_password_hash(post_body.password)  
    # Creating new user
    new_user = models.User(**post_body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GET request to find user by id: users/{id}  (200 OK default) 
@router.get("/{id}",
            response_model= schemas.User_response)
def get_user(id: int,
             db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail= f"User with id: {str(id)} was not found")


