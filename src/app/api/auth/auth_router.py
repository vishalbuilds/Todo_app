from datetime import timedelta
from database.crud_common import GenericCRUD
from typing import Annotated, Literal
from fastapi import APIRouter, Depends, Query, HTTPException
from database.models import *
from utils.id_generator import create_id
from starlette import status
from database.db_session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas_user import *
from utils.results import Result
from utils.phone_validator import PhoneNumberValidator
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from utils.jwt_handler import JWTHandler



ACCESS_SECRET_KEY = "xhS4oXm2YAmy77Fi0nHfJDlSLnNrCtRtr0dTZ4ZnjkM"
REFRESH_SECRET_KEY="ri3PML6FuYlIGeOGK5DL1FsIexoYOSuLoJlbh_B6POI"
token_obj=JWTHandler(REFRESH_SECRET_KEY,ACCESS_SECRET_KEY)




router=APIRouter()

AsyncDB = Annotated[AsyncSession, Depends(get_db)]

USER_ROLE=Literal["admin","manager","user"]

bcrypt_context= CryptContext(schemes=['bcrypt'],deprecated="auto")






#create user 
@router.post("/create_user/",status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,session:AsyncDB):
    crud_obj= GenericCRUD(User,session)

    check_result=await crud_obj.get_one({"username":create_user_request.username})
    if check_result:
        return Result.already_exists(data=create_user_request,message="This username is already taken. Please choose a different one")
    
    create_user_model=User(**create_user_request.model_dump(exclude={"password","phone"}))
    create_user_model.id = create_id()
    create_user_model.hashed_password=bcrypt_context.hash(create_user_request.password)
    create_user_model.account_status="active"
    if PhoneNumberValidator.validate(create_user_request.phone):
        create_user_model.phone=create_user_request.phone
    else:
       return Result.validation_failed(data=create_user_request.phone,message="invalid phone nubmer, Please enter correct phone number")

    create_result= await crud_obj.create(create_user_model)
    return Result.success(data=CreateUserResponse.model_validate(create_result),message="User created successfully")



#get token
@router.post("/login/", status_code=status.HTTP_202_ACCEPTED)
async def login(login_request:UserLoginRequest , session: AsyncDB):
    crud_user_obj = GenericCRUD(User, session)
    user_details = await crud_user_obj.get_one({"username":login_request.username})
    #process user athentication
    if not user_details:
        return Result.not_found(data=login_request.username, message="Username does not exist. Please sign up to continue")

    if user_details.account_status in ["deactivated", "deleted", "blocked"]:
        status_msg = {
            "deactivated": "Username is deactivated. Please re-activate username to continue",
            "deleted": "Username is deleted. Please re-create account to continue",
            "blocked": "Username blocked by admin. Access unauthorized"
        }
        return Result.unauthorized(data=login_request.username, message=status_msg[user_details.account_status])

    if not bcrypt_context.verify(login_request.password, user_details.hashed_password) and user_details.account_status == "active":
        return Result.unauthorized(data=login_request.username, message="Incorrect password. Please try again")

    #issues access and refresh token
    #used to create payload for refresh token
    refresh_session_jti_id=create_id()
    refresh_token_claims = {
        "username": user_details.username,
        "firstname": user_details.firstname,
        "lastname": user_details.lastname,
        "role": user_details.role,
        "jti": create_id()
    }
    #create refresh token

    refresh_token=token_obj.create_refresh_token(refresh_token_claims, timedelta(minutes=1))
    #used to create row in user_session table in database
    user_session_request=RefreshSessionRequest(
        id =create_id(),
        user_id = user_details.id,
        session_id= refresh_token_claims["jti"],
        device_id =login_request.device_id,
        user_agent= login_request.user_agent,
        ip_address=login_request.ip_address,
        hashed_refresh_token=bcrypt_context.hash(refresh_token),
        is_active=True
    )
    user_session_model=User_session(**user_session_request.model_dump())
    await GenericCRUD(User_session,session).create(user_session_model)

    #access token claims
    access_token_claims = {
        "username": user_details.username,
        "firstname": user_details.firstname,
        "lastname": user_details.lastname,
        "role": user_details.role
    }
    access_token=token_obj.create_access_token(access_token_claims, timedelta(seconds=10))
    
    response_data = UserLoginResponse.model_validate(
        {
        "id":user_details.id,
        "username": user_details.username,  
        "firstname": user_details.firstname,
        "lastname": user_details.lastname,
        "role": user_details.role,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    )
    return Result.success(data=response_data, message="Authentication successful. You are now logged in")


@router.post("/renew_access_token/")
async def renew_access_token(Refresh_token_request: , session: AsyncDB):





#reset password, re-active account, get-me-info, delete-acc, deactive account, renew access token