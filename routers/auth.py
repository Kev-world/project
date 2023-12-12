from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from annotated_types import Annotated
from databases.mongoDB import db
from securities.auth_bearer import JWTBearer
from bson import ObjectId
from pydantic import BaseModel, Field
from bson import ObjectId
import requests
import httpx


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

class User(BaseModel):
    id: str = Field(None, alias='_id')
    email: str
    password: str
    roles: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "email": "test@gmail.com",
                "password": "yourhashedpassword",
                "roles": []
            }
        }
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }

class LoginRequest(BaseModel):
    email: str = Field(min_length=10)
    password: str = Field(min_length=6)

async def get_db():
    try:
        yield db
    finally:
        pass

# oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

@router.get('/user/current_user')
async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('userId')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return { 'id': user_id }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
@router.get("/user/{_id}", response_model=User, dependencies=[Depends(JWTBearer())])    
async def validate_user(_id: str, db=Depends(get_db)):
    try:
        oid = ObjectId(_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId format.")

    user_doc = await db['userdocuments'].find_one({"_id": oid})
    if user_doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    user_doc['_id'] = str(user_doc['_id'])
    user = User(**user_doc)
    return user

# @router.get('/users')
# async def get_all(db=Depends(get_db)):
#     li = []
#     user = await db.get_collection('userdocuments').find().to_list(100)
#     for u in user:
#         u['_id'] = str(u['_id'])
#         li.append(User(**u))
#     return li


@router.post('/users/login')
async def login(req: LoginRequest):
    api_url = 'http://localhost:3001/auth/login'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url=api_url, params=req.model_dump())
            print(response)
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))