from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta

from pydantic import EmailStr
from . import schemas
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(payload_data_dict:dict):
    payload = payload_data_dict.copy()   # Created copy of dictionary- data
    # Adding expire component to this dictionary copy
    expire= datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    # Creating jwt token
    encoded_jwt= jwt.encode(payload, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str,
                       exception_for_invalid_credentials):
    try:
        # Extracting payload data (email in this case) from the token
        # Decode jwt token to get the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        email : EmailStr = payload.get("email")
        if email:
            payload_data = schemas.Access_token_Payload_data(username= email)
            return payload_data
        else:
            raise exception_for_invalid_credentials
    except JWTError:
        raise exception_for_invalid_credentials
    

# Function to know current logged in user from token
# This function will be added as dependancy in other functions  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(token: str = Depends(oauth2_scheme)):
    exception_for_invalid_credentials = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers= {"WWW-Authenticate": "Bearer"}
        )
    return verify_access_token(token, exception_for_invalid_credentials)
