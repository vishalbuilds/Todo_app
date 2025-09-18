from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class CreateUserRequest(BaseModel):
    username: str
    firstname: Optional[str]=None
    lastname: Optional[str]=None
    role: Optional[str]=None
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