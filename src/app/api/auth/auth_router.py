

from database.crud_common import CRUD
from typing import Annotated, Literal
from fastapi import APIRouter, Depends, Query, HTTPException
from database.models import User
from utils.id_generator import create_id
from starlette import status
from database.db_session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas_user import CreateUserRequest,CreateUserResponse,AuthUserResponse
from utils.results import Result
from utils.phone_validator import PhoneNumberValidator
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter()

AsyncDB = Annotated[AsyncSession, Depends(get_db)]

USER_ROLE=Literal["admin","manager","user"]

bcrypt_context= CryptContext(schemes=['bcrypt'],deprecated="auto")




#create user 
@router.post("/create_user/",status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,session:AsyncDB):
    crud_obj= CRUD(User,session)

    check_result=await crud_obj.get_by_id_pk_unqie_return ("username",create_user_request.username)
    if check_result:
        return Result.already_exists(data=create_user_request,message="This username is already taken. Please choose a different one")
    
    create_user_model=User(**create_user_request.model_dump(exclude={"password","phone"}))
    create_user_model.id = create_id()
    create_user_model.hashed_password=bcrypt_context.hash(create_user_request.password)
    create_user_model.is_active=True
    if PhoneNumberValidator.validate(create_user_request.phone):
        create_user_model.phone=create_user_request.phone
    else:
       return Result.validation_failed(data=create_user_request.phone,message="invalid phone nubmer, Please enter correct phone number")

    create_result= await crud_obj.create_unique(create_user_model)
    return Result.success(data=CreateUserResponse.model_validate(create_result),message="User created successfully")

#get token
@router.post("/get_token/",status_code=status.HTTP_202_ACCEPTED)
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],session:AsyncDB):
    crud_obj= CRUD(User,session)
    check_user=await crud_obj.get_by_id_pk_unqie_return("username",form_data.username)
    if not check_user:
        return Result.not_found(data=form_data.username,message="Username does not exist. Please sign up to continue")
    if not bcrypt_context.verify(form_data.password,check_user.hashed_password):
        return Result.unauthorized(data=form_data.username,message="Incorrect password. Please try again")
    return Result.success(data=AuthUserResponse.model_validate(check_user),message="Authentication successful. You are now logged in")