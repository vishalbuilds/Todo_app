
from sqlalchemy import create_engine, VARCHAR, TIMESTAMP, func, ForeignKey
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
    due_date: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)

# Typed annotated string types with defined VARCHAR lengths and nullability constraints

str_50_not_null = Annotated[str, mapped_column(VARCHAR(50), nullable=False)]
str_50_nullable = Annotated[str, mapped_column(VARCHAR(50))]
str_50_optional = Annotated[Optional[str], mapped_column(VARCHAR(50))]

str_225_pk= Annotated[str, mapped_column(VARCHAR(225), nullable=False,primary_key=True)]
str_225_pk_unique= Annotated[str, mapped_column(VARCHAR(225), nullable=False,primary_key=True,unique=True)]

str_225_not_null = Annotated[str, mapped_column(VARCHAR(225), nullable=False)]
str_225_nullable = Annotated[str, mapped_column(VARCHAR(225))]
str_225_optional = Annotated[Optional[str], mapped_column(VARCHAR(225))]


# ORM model definition for List table combining Base and timestamp fields
class List(Base, TimeStampMixin):
    id: Mapped[str_225_pk_unique] 
    title: Mapped[str_225_pk]
    description: Mapped[str_225_nullable]
    status: Mapped[str_50_nullable]
    priority: Mapped[str_50_nullable]
    tags: Mapped[dict]=mapped_column(JSON)
    # Foreign key referencing users.id with on-delete SET NULL cascade behavior
    user_id: Mapped[str] = mapped_column(VARCHAR(225), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)


class User(Base):
    id: Mapped[str_225_pk_unique]




