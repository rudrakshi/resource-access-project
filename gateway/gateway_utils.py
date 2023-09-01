from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mock data used for POC - to be replaced by database in real implementation
users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "$2b$12$PCGepZjLanu5Ewf0AQwOHuUFlR8s8fpmztvp8qMw0m5.yal8uKm4O",
        "disabled": False,
        "scope": ["read"]
    },
    "janedoe": {
        "username": "janedoe",
        "hashed_password": "$2b$12$PCGepZjLanu5Ewf0AQwOHuUFlR8s8fpmztvp8qMw0m5.yal8uKm4O",
        "disabled": False,
        "scope": ["read","write"]
    },
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$PCGepZjLanu5Ewf0AQwOHuUFlR8s8fpmztvp8qMw0m5.yal8uKm4O",
        "disabled": False,
        "scope": ["read","write","admin"]
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    Returns new access token

    Parameters
    ----------
    data : dict, mandatory
        Data like user, access scope, etc to be embedded in the token
    
    expires_delta : timedelta
        Validity time of the token in minutes 

    Returns
    -------
    Encoded token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    """
    Returns user object if it exists otherwise False

    Parameters
    ----------
    username : str, mandatory
        user name of the user

    password : str, mandatory
        password of the user

    Returns
    -------
    User object: If user exists

    False: If user does not exists
    """
    user = users_db[username]

    if not user:
        return False
    if not pwd_context.verify(password, user["hashed_password"]):
        return False
    return user

def validate_token(token):
    """
    Validate and decode the token

    Parameters
    ----------
    resource_id : str, mandatory
        identification number of the resource

    Returns
    -------
    Decoded token data

    Raises
    ------
    HTTPException: 400
        Token is not valid or has expired
    """
    try:
      token_data = jwt.decode(token, SECRET_KEY,ALGORITHM)
    except Exception as e:
      if "expired" in str(e):
        raise HTTPException(status_code=400, detail={"status": "error", "message": "Token expired"})
      else:
        raise HTTPException(status_code=400, detail={"status": "error", "message": "Exception: " + str(e)})
    return token_data