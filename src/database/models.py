
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
    is_active : Mapped[bool]=mapped_column(BOOLEAN,nullable=false,default=true)




