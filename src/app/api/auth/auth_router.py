
from re import S
from typing import Annotated, Literal
from fastapi import APIRouter, Depends, Query,HTTPException
from database.models import User
from utils.id_generator import create_id
from database.crud_user import CRUD_users
from starlette import status
from database.db_session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas_user import CreateUserRequest
from utils.results import Result
from utils.phone_validator import PhoneNumberValidator


router=APIRouter()

AsyncDB = Annotated[AsyncSession, Depends(get_db)]





@router.post("/create_user/",status_code=status.HTTP_200_OK)
async def create_user(create_user_request: CreateUserRequest,session:AsyncDB):
    crud_obj= CRUD_users(session)

    check_result=await crud_obj.get_user_by_key_pk("username",create_user_request.username)
    if check_result:
        return Result.already_exists(data=create_user_request,message="This username is already taken. Please choose a different one")
    
    create_user_model=User(**create_user_request.model_dump(exclude={"password","phone"}))
    create_user_model.id = create_id()
    create_user_model.hashed_password=create_user_request.password
    create_user_model.is_active=True
    if PhoneNumberValidator.validate(create_user_request.phone):
        create_user_model.phone=create_user_request.phone
    else:
       return Result.validation_failed(data=create_user_request.phone,message="invalid phone nubmer, Please enter correct phone number")

    create_result= await CRUD_users(session).create_user(create_user_model)
    return Result.success(data=create_result,message="User created successfully")


