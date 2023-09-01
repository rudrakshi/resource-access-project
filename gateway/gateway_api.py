from fastapi import FastAPI, Request, Security, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .gateway_utils import *
import requests
import os

gate = FastAPI(debug=True)

host_url = os.getenv('API_URL',"http://localhost:8282/")

class Token(BaseModel):
    """
    Token(access_token, token_type)
  
    A class to represent a token.
    
    ...
    
    Attributes
    ----------
    access_token : str
        encoded information used to identify and authorize a user
    token_type : str
        type of the token
    """
    access_token: str
    token_type: str

@gate.get("/api/{path:path}")
async def read_request(request: Request, path: str, header_token: str = Security(oauth2_scheme)):
  """
  Returns requested information when a valid token with required permissions is provided

  Parameters
  ----------
  path : str, mandatory
      requested path of the API

  header_token: str
      authorisation header with a Bearer token

  request: Request
      request object with other information of the HTTP call

  Returns
  -------
  Streams the response object received by calling the given path of the API

  Raises
  ------
  HTTPException: 400
      the token has expired or other details

  HTTPException: 403
      the user is not allowed to access this path
  """
  token_info =validate_token(header_token)
  if "read" in token_info["scope"]:
    headers = {k: v for k, v in request.headers.items()}
    headers.pop('host')
    headers.pop('accept-encoding')

    res = requests.get(f'{host_url}{path}', params=request.query_params, headers=headers, stream=True)

    return StreamingResponse(
        res.iter_lines(),
        status_code=res.status_code,
        headers=headers,
    )
  else:
     raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is not allowed",
            headers={"WWW-Authenticate": "Bearer"},
        )
     

@gate.post("/api/{path:path}")
async def post_request(path: str, request: Request, header_token: str = Security(oauth2_scheme)):
  """
  Returns outcome of post request when a valid token with required permissions is provided

  Parameters
  ----------
  path : str, mandatory
      requested path of the API

  header_token: str
      authorisation header with a Bearer token

  request: Request
      request object with other information of the HTTP call

  Returns
  -------
  Streams the response object received by calling the given path of the API

  Raises
  ------
  HTTPException: 400
      the token has expired or other details

  HTTPException: 403
      the user is not allowed to access this path
  """  
  token_info =validate_token(header_token)
  if "write" in token_info["scope"]:
    headers = {k: v for k, v in request.headers.items()}  
    headers.pop('host')
    headers.pop('accept-encoding')
    headers.pop('content-length')
    request_data = await request.json()
    res = requests.post(f'{host_url}{path}', params=request.query_params, headers=headers, json=request_data)

    return StreamingResponse(
        res.iter_lines(),
        status_code=res.status_code,
        headers=headers,
    )
  else:
     raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is not allowed",
            headers={"WWW-Authenticate": "Bearer"},
        )

@gate.put("/api/{path:path}")
async def put_request(path: str, request: Request, header_token: str = Security(oauth2_scheme)):
  """
  Returns outcome of update request when a valid token with required permissions is provided

  Parameters
  ----------
  path : str, mandatory
      requested path of the API

  header_token: str
      authorisation header with a Bearer token

  request: Request
      request object with other information of the HTTP call

  Returns
  -------
  Streams the response object received by calling the given path of the API

  Raises
  ------
  HTTPException: 400
      the token has expired or other details

  HTTPException: 403
      the user is not allowed to access this path
  """
  token_info =validate_token(header_token)
  if "write" in token_info["scope"]:
    headers = {k: v for k, v in request.headers.items()}
    headers.pop('host')
    headers.pop('accept-encoding')
    headers.pop('content-length')
    request_data=await request.json()

    res = requests.put(f'{host_url}{path}', params=request.query_params, headers=headers, json=request_data)

    return StreamingResponse(
        res.iter_lines(),
        status_code=res.status_code,
        headers=headers,
    )
  else:
     raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is not allowed",
            headers={"WWW-Authenticate": "Bearer"},
        )

@gate.delete("/api/{path:path}")
async def delete_request(request: Request, path: str, header_token: str = Security(oauth2_scheme)):
  """
  Returns response of requested delete operation when a valid token with required permissions is provided

  Parameters
  ----------
  path : str, mandatory
      requested path of the API

  header_token: str
      authorisation header with a Bearer token

  request: Request
      request object with other information of the HTTP call

  Returns
  -------
  Streams the response object received by calling the given path of the API

  Raises
  ------
  HTTPException: 400
      the token has expired or other details

  HTTPException: 403
      the user is not allowed to access this path
  """
  token_info =validate_token(header_token)
  if "admin" in token_info["scope"]:
    headers = {k: v for k, v in request.headers.items()}
    headers.pop('host')
    headers.pop('accept-encoding')

    res = requests.delete(f'{host_url}{path}', params=request.query_params, headers=headers, stream=True)

    return StreamingResponse(
        res.iter_lines(),
        status_code=res.status_code,
        headers=headers,
    )
  else:
     raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access is not allowed",
            headers={"WWW-Authenticate": "Bearer"},
        )

@gate.post("/token", response_model=Token)
async def login_for_access_token(username: str, password: str):
    """
    Returns a valid token if user credentials are correct

    Parameters
    ----------
    username : str, mandatory
        requested path of the API

    password: str, mandatory
        authorisation header with a Bearer token

    Returns
    -------
    Returns the token object

    Raises
    ------
    HTTPException: 404
        User not found

    HTTPException: 401
        User is not authorised
    """
    try:
      user = authenticate_user(username, password)
      if not user:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Incorrect username or password",
              headers={"WWW-Authenticate": "Bearer"},
          )
      access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      access_token = create_access_token(
          data={"subject": user["username"], "extra_info": "short lived token","scope": user["scope"]}, expires_delta=access_token_expires
      )
      return {"access_token": access_token, "token_type": "bearer"}
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found.")
