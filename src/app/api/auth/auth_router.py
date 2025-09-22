from datetime import timedelta,timezone
from encodings.rot_13 import rot13
from urllib import response
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



ACCESS_SECRET_KEY = "xhS4oXm2YAmy77Fi0nHfJDlSLnNrCtRtr0dTZ4ZnjkM"   #public key
REFRESH_SECRET_KEY="ri3PML6FuYlIGeOGK5DL1FsIexoYOSuLoJlbh_B6POI"   #private key
token_obj=JWTHandler(REFRESH_SECRET_KEY,ACCESS_SECRET_KEY)




router=APIRouter()

AsyncDB = Annotated[AsyncSession, Depends(get_db)]

USER_ROLE=Literal["admin","manager","user"]

bcrypt_context= CryptContext(schemes=['bcrypt'],deprecated="auto")






#create user 
@router.post("/create_user/",status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest,session:AsyncDB):
    crud_obj= GenericCRUD(User,session)
    #check if username already exists
    check_result=await crud_obj.get_one({"username":create_user_request.username})
    #username already exists or not
    if check_result:
        return Result.already_exists(data=create_user_request,message="This username is already taken. Please choose a different one")
    #update model and hash password to create user
    create_user_model=User(**create_user_request.model_dump(exclude={"password","phone"}))
    create_user_model.id = create_id()
    create_user_model.hashed_password=bcrypt_context.hash(create_user_request.password)
    create_user_model.account_status="active"
    #validate phone number
    if PhoneNumberValidator.validate(create_user_request.phone):
        create_user_model.phone=create_user_request.phone
    else:
       return Result.validation_failed(data=create_user_request.phone,message="invalid phone nubmer, Please enter correct phone number")
    #create user
    create_result= await crud_obj.create(create_user_model)
    final_response=CreateUserResponse.model_validate(
        create_result
    )

    return Result.success(data=final_response,message="User created successfully")



#user login and issue access and refresh token
@router.post("/login/", status_code=status.HTTP_202_ACCEPTED)
async def login(login_request:UserLoginRequest , session: AsyncDB):
    crud_user_obj = GenericCRUD(User, session)
    crud_session_obj=GenericCRUD(User_session,session)
    #check if username exists
    user_details = await crud_user_obj.get_one({"username":login_request.username})
    #username does not exist
    if not user_details:
        return Result.not_found(data=login_request.username, message="Username does not exist. Please sign up to continue")
    #check if account is active
    if user_details.account_status in ["deactivated", "deleted", "blocked"]:
        status_msg = {
            "deactivated": "Username is deactivated. Please re-activate username to continue",
            "deleted": "Username is deleted. Please re-create account to continue",
            "blocked": "Username blocked by admin. Access unauthorized"
        }
        return Result.unauthorized(data=login_request.username, message=status_msg[user_details.account_status])
    #check if password is correct
    if not bcrypt_context.verify(login_request.password, user_details.hashed_password) and user_details.account_status == "active":
        return Result.unauthorized(data=login_request.username, message="Incorrect password. Please try again")

    #issues access and refresh token
    #used to create payload for refresh token
    refresh_token_claims = {
        "id":create_id(),
        "user_id": user_details.id,
        "username": user_details.username,
        "jti": create_id(),
        "device_id":create_id()
    }
    #create refresh token
    expire_delta=timedelta(minutes=5)
    refresh_token=token_obj.create_refresh_token(refresh_token_claims, expire_delta)
    #used to create row in user_session table in database
    user_session_request=RefreshSessionRequest(
        id =refresh_token_claims["id"],
        user_id = user_details.id,
        username=user_details.username,
        session_id= refresh_token_claims["jti"],
        device_id = refresh_token_claims["device_id"],
        user_agent= login_request.user_agent,
        ip_address=login_request.ip_address,
        hashed_refresh_token=bcrypt_context.hash(refresh_token),
        is_active=True,
        is_logout=False,
        expire_date=datetime.now(tz=timezone.utc)+expire_delta
    )

    #create user session in database with pydantic model
    user_session_model=User_session(**user_session_request.model_dump())
    # create user session in database
    await crud_session_obj.create(user_session_model)

    #access token claims
    access_token_claims = {
        "username": user_details.username,
        "firstname": user_details.firstname,
        "lastname": user_details.lastname,
        "role": user_details.role
    }
    #create access token
    access_token=token_obj.create_access_token(access_token_claims, timedelta(seconds=20))
    
    final_response = UserLoginResponse.model_validate(
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
    return Result.success(data=final_response, message="Authentication successful. You are now logged in")

#renew access token
@router.post("/renew_access_token/")
async def renew_access_token(renew_access_token_request: RenewAccessTokenRequest, session: AsyncDB):
    crud_session_obj=GenericCRUD(User_session,session)
    #check if grant_type is refresh_token
    if renew_access_token_request.grant_type!="refresh_token":
        return Result.internal_error(data=renew_access_token_request,message="Renew token failed. wrong grant_type")
    #verify refresh token
    refresh_token_payload=token_obj.verify_access_token(renew_access_token_request.refresh_token,refresh=True)
    #check if refresh token is valid
    if not refresh_token_payload["verified"]:
        return Result.unauthorized(data=renew_access_token_request,message=f"refresh token verification failed. Error :{refresh_token_payload}")
    #check if refresh token exists in database
    user_session_details= await crud_session_obj.get_one({"id":refresh_token_payload["payload"]["id"]})
    #check if refresh token is Exists in database
    if not user_session_details:
        return Result.unauthorized(data=renew_access_token_request,message="refresh token not exists. Failed to renew access_token.")
    #check if user logout
    if user_session_details.is_logout:
        return Result.unauthorized(data=renew_access_token_request,message="User is logged out. Failed to renew access_token.")
    #check if refresh token is active or not
    if not user_session_details.is_active:
        return Result.unauthorized(data=renew_access_token_request,message="Expired refresh_token. Failed to renew access_token.")
    #check if refresh token is expired or not by comparing expire_date in db and exp in token payload
    if user_session_details.device_id!=refresh_token_payload["payload"]["device_id"] and user_session_details.expire_date<refresh_token_payload["payload"]["exp"]:
        await crud_session_obj.update({"id":refresh_token_payload.id},{"is_active":False,"expire_date":datetime.now(tz=timezone.utc)})
        return Result.unauthorized(data=renew_access_token_request,message="Expired refresh_token. Failed to renew access_token.")
    #check if refresh token jti matches with session id in db where jti should be same as session id
    if user_session_details.session_id!=refresh_token_payload["payload"]["jti"]:
        await crud_session_obj.update({"id":refresh_token_payload.id},{"is_active":False,"expire_date":datetime.now(tz=timezone.utc)})
        return Result.unauthorized(data=renew_access_token_request,message="Expired refresh_token. Failed to renew access_token.")
    #check if refresh token belongs to same user
    if user_session_details.user_id!=refresh_token_payload["payload"]["user_id"]:
        await crud_session_obj.update({"id":refresh_token_payload.id},{"is_active":False,"expire_date":datetime.now(tz=timezone.utc)})
        return Result.unauthorized (data=renew_access_token_request,message="Token belongs to a different user. Failed to renew access_token. Token marked as expired")
    
    #check if refresh token matches with hashed refresh token in db    
    if not bcrypt_context.verify(renew_access_token_request.refresh_token,user_session_details.hashed_refresh_token):
        await crud_session_obj.update({"id":refresh_token_payload.id},{"is_active":False,"expire_date":datetime.now(tz=timezone.utc)})
        return Result.unauthorized (data=renew_access_token_request,message="Invalid refresh_token. Failed to renew access_token. Token marked as expired")

    #check if user account is active
    user_details = await GenericCRUD(User, session).get_one({"id":user_session_details.user_id})
    #check user account status either deactivated, deleted or blocked
    if not user_details or user_details.account_status in ["deactivated", "deleted", "blocked"]:
        await crud_session_obj.update({"id":refresh_token_payload.id},{"is_active":False,"expire_date":datetime.now(tz=timezone.utc)})
        status_msg = {
            "deactivated": "Username is deactivated. Please re-activate username to continue",
            "deleted": "Username is deleted. Please re-create account to continue",
            "blocked": "Username blocked by admin. Access unauthorized"
        }
        return Result.unauthorized(data=renew_access_token_request, message=f"User account not active. {status_msg[user_details.account_status]}. Token marked as expired")

    #check access token for sessions created for single user in single device
    device_sessions=crud_session_obj.get_all({"user_id":user_session_details.user_id,"is_active":True,"device_id":refresh_token_payload["payload"]["device_id"]},order_by="created_at")
    #limit no of active session to 5
    if len(device_sessions)>5:
        oldest_session=device_sessions[0]
        await crud_session_obj.update({"id":oldest_session.id},{"is_active":False,"expire_date":datetime.now(tz=timezone.utc)}) 

    #check new access token for all sessions created for single user in all devices
    all_sessions=crud_session_obj.get_all({"user_id":user_session_details.user_id,"is_active":True},order_by="created_at")
    #limit no of active all session to 10
    if len(all_sessions)>10:
        oldest_session=all_sessions[0]
        await crud_session_obj.update({"id":oldest_session.id},{"is_active":False,"expire_date":datetime.now(tz=timezone.utc)}) 

    #access token claims
    crud_user_obj = GenericCRUD(User, session)
    user_details = await crud_user_obj.get_one({"id":user_session_details.user_id})
    access_token_claims = {
        "username": user_details.username,
        "firstname": user_details.firstname,
        "lastname": user_details.lastname,
        "role": user_details.role
    }
    access_token=token_obj.create_access_token(access_token_claims, timedelta(seconds=20))

    final_response=RenewAccessTokenResponse.model_validate(
        {
        "access_token":access_token
        }
    )

    return Result.success(data=final_response,message="Refresh_token succesfully. Issuing new access_token")

#logout user and mark refresh token as inactive 
@router.post("/logout/")
async def logout(logout_request: LogoutRequest, session: AsyncDB):
    refresh_token_payload=token_obj.verify_access_token(logout_request.refresh_token,refresh=True)
    #check if refresh token is valid
    if not refresh_token_payload["verified"]:
        return Result.unauthorized(data=logout_request,message=f"refresh token verification failed. Error :{refresh_token_payload}")
    user_session_details=GenericCRUD(User_session,session).get_one({"id":refresh_token_payload["payload"]["id"]})
    # check if refresh token is Exists in database
    if not user_session_details:
        return Result.unauthorized(data=logout_request,message="refresh token not exists. Failed to logout.")   
    #check if refresh token is active or not
    if not user_session_details.is_active:
        return Result.unauthorized(data=logout_request,message="Expired refresh_token. Failed to logout.")
    #check if user logout or not
    if user_session_details.is_logout:
        return Result.unauthorized(data=logout_request,message="User already logged out.")
    #mark refresh token as inactive and logout true
    await user_session_details.update({"id":refresh_token_payload["payload"]["id"]},{"is_active":False,"is_logout":True,"expire_date":datetime.now(tz=timezone.utc)})
    final_response=LogoutResponse.model_validate(
        {
            "user_id":user_session_details.user_id
        }
    )
    return Result.success(data=final_response,message="User logged out successfully.")

#reset password
@router.post("/reset_password/")
async def reset_password():
    pass
#re-active account
@router.post("/reactivate_account/")
async def reactivate_account():
    pass   
#get me info
@router.get("/get_me/")
async def get_me():
    pass   
#delete account 
@router.delete("/delete_account/")
async def delete_account(): 
    pass   
#deactivate account     
@router.post("/deactivate_account/")
async def deactivate_account():
    pass







#reset password, re-active account, get-me-info, delete-acc, deactive account, 