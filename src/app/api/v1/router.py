from typing import Annotated
from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import db_session
from database.db_session import get_db
from database.crud import CRUD_items

router=APIRouter()

session=Annotated[AsyncSession,Depends(get_db)]

@router.get("/books/")
async def get_books(key:str, value: str, session:session):
    crud_ops=CRUD_items(session)
    response=await crud_ops.get_todo_by_key_pk(key,value)
    return response