from weakref import ref
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional,Literal


class CreateUserRequest(BaseModel):
    username: str
    firstname: Optional[str]=None
    lastname: Optional[str]=None
    role: Optional[Literal['admin', 'user', 'manager']] = 'user'
    password: str
    email: Optional[EmailStr]=None
    phone:Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "vishal_singh",
                "firstname": "Vishal",
                "lastname": "Singh",
                "role": "user",
                "password": "India@12345",
                "email": "vishal.singh@example.in",
                "phone": "+919876543210"
            }
        }
    } 

class CreateUserResponse(BaseModel):
    id: str
    username: str
    firstname: str
    lastname: str
    phone: str
    role: str 

    model_config = ConfigDict(from_attributes=True)

class UserLoginRequest(BaseModel):
    username:str
    password: str
    device_id: str
    ip_address: str
    ip_address:str
    user_agent: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "vishal_singh",
                "password": "India@12345",
                "device_id": "abc123xyz",
                "ip_address": "127.0.0.1:8000",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            }
        }
    } 

class UserLoginResponse(BaseModel):
    id: str
    username: str
    firstname: str
    lastname: str
    role: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)




class RefreshSessionRequest(BaseModel):
    id: str
    user_id: str
    username: str
    session_id: str
    device_id: str
    user_agent: str
    ip_address: str
    hashed_refresh_token: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)



class RenewAccessTokenRequest(BaseModel):
    grant_type:str
    refresh_token: str
    ip_address: str
    user_agent:str
    model_config = {
        "json_schema_extra": {
            "example": {
                "grant_type": "refresh_token",
                "refresh_token": "---",
                "ip_address": "127.0.0.1:8000",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            }
        }
    }
class RenewAccessTokenResponse(BaseModel):
    grant_type:str = "access_token"
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)

class LogoutRequest(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "user123",
                "access_token": "---",
                "refresh_token": "--"
            }
        }
    }

class LogoutResponse(BaseModel):
    user_id: str

    model_config = ConfigDict(from_attributes=True)