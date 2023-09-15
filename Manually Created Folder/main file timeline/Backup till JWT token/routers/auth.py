from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db


router= APIRouter(tags= ["Authentication"])

@router.post("/login")
def authentication (post_body: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(get_db)):
    user_requested = db.query(models.User).filter(post_body.username == models.User.email).first()
    if user_requested:
        if utils.verify_password(post_body.password, user_requested.password):
            # calling function to create access token
            # in dictionary, we can decide which arguments to pass. It should be a unique identifier of the user.
            access_token = oauth2.create_access_token(payload_data_dict= {"email": post_body.username})
            # return format is as following. This type of token is called bearer token
            return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= "Invalid credentials")