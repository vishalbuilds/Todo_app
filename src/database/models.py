
from email.mime import base
from enum import unique
from sqlalchemy import Nullable, create_engine, VARCHAR, TIMESTAMP, false, func, ForeignKey, true ,BOOLEAN
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped
from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy.dialects.postgresql import JSON


# Variable
SERVER_DEFAULT_TIMESTAMP = func.now()

# Mixin to automatically generate table names as lowercase plural form of class name
class TableNameMixin:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

# Base class for ORM models, combining SQLAlchemy DeclarativeBase and table name mixin
class Base(DeclarativeBase, TableNameMixin):
    pass


# Mixin providing common timestamp columns with default current time handling
class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=SERVER_DEFAULT_TIMESTAMP
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=SERVER_DEFAULT_TIMESTAMP, onupdate=func.now()
    )
class DueTimeMixin:
    due_date: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)

# Typed annotated string types with defined VARCHAR lengths and nullability constraints

str_20= Annotated[str, mapped_column(VARCHAR(20),nullable=false)]
str_20_optional = Annotated[Optional[str], mapped_column(VARCHAR(20))]


str_50= Annotated[str, mapped_column(VARCHAR(50),nullable=false)]
str_50_optional = Annotated[Optional[str], mapped_column(VARCHAR(50))]

str_225 = Annotated[str, mapped_column(VARCHAR(225),nullable=false)]
str_225_optional = Annotated[Optional[str], mapped_column(VARCHAR(225))]



# ORM model definition for List table for todo
class List(Base, TimeStampMixin, DueTimeMixin):
    id: Mapped[str_50]= mapped_column(unique=True,primary_key=True) 
    title: Mapped[str_225]= mapped_column(primary_key=true)
    description: Mapped[str_225_optional]
    status: Mapped[str_20_optional]
    priority: Mapped[str_20_optional]
    tags: Mapped[dict]=mapped_column(JSON)
    # Foreign key referencing users.id with on-delete SET NULL cascade behavior
    owner_id: Mapped[str_20_optional] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))

# ORM model definition for List table for user base
class User(Base,TimeStampMixin):
    id: Mapped[str_50]= mapped_column(unique=True,primary_key=True) 
    username: Mapped[str_20]=mapped_column(primary_key=true,unique=true)
    firstname: Mapped[str_20_optional]
    lastname: Mapped [str_20_optional]
    role: Mapped [str_20]
    hashed_password: Mapped [str_225]
    email: Mapped [str_50_optional] =mapped_column(unique=true)
    phone: Mapped [str_20_optional] =mapped_column(unique=true)
    account_status :Mapped[str_20]=mapped_column(default=true)

class User_session(Base, TimeStampMixin):
    id: Mapped[str_50]=mapped_column(unique=True,primary_key=True)
    user_id: Mapped[str_50]=mapped_column(ForeignKey('users.id'),primary_key=True)
    session_id: Mapped[str_50]  #same as jti id sent to refresh token
    device_id: Mapped[str_50_optional]
    user_agent:Mapped[str_225_optional] #check below dict user_agents
    ip_address:Mapped[str_50_optional]
    hashed_refresh_token: Mapped[str_225_optional]
    is_active:Mapped[bool]=mapped_column(nullable=False)



user_agents = {
    "chrome_windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "firefox_windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "safari_mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "edge_windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    "iphone": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
              "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "android": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
    "curl": "curl/8.3.1"
}




