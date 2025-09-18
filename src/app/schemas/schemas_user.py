from pydantic import BaseModel, EmailStr, ConfigDict
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
                "role": "Owner",
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

class AuthUserResponse(BaseModel):
    id: str
    username: str
    firstname: str
    lastname: str
    role: str

    model_config = ConfigDict(from_attributes=True)
