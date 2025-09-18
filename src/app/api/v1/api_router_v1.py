from typing import Annotated, Literal
from fastapi import APIRouter, Depends, Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_session import get_db
from database.crud_todo import CRUD_todo
from utils.id_generator import create_id
from app.schemas.schemas_todo import TodoRequest
from starlette import status
from database.models import List



#variable
KEY_GET=Literal["id", "title"]
KEY_UPDATE=Literal["title","description", "status", "priority", "tags", "owner_id"]
DESC_UPDATE="Filter key: id | title | description | status | priority | tags | owner_id"

router = APIRouter()

AsyncDB = Annotated[AsyncSession, Depends(get_db)]


@router.get("/get_todo/", status_code=status.HTTP_200_OK)
async def get_todo(key: Annotated[KEY_GET, Query(description="Filter key: id | title")], value: Annotated[str, Query(min_length=1, description="Filter value (non-empty)")], session: AsyncDB):
    return await CRUD_todo(session).get_todo_by_key_pk(key, value)


@router.post("/create_todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(session: AsyncDB, todo_request: TodoRequest):
    todo_model = List(**todo_request.model_dump())
    todo_model.id = create_id()
    todo_model.owner_id = (
        todo_model.owner_id if isinstance(todo_model.owner_id, str) else None
    )
    return await CRUD_todo(session).add_todo(todo_model)

@router.put("/update_todo/", status_code=status.HTTP_202_ACCEPTED)
async def update_todo(id: Annotated[str, Query(description="Filter key: id")], key: Annotated[KEY_UPDATE, Query(description=DESC_UPDATE)], value: Annotated[str, Query(min_length=1, description="Filter value (non-empty)")], session: AsyncDB):
    return await CRUD_todo(session).update_todo(id, key, value)



@router.delete("/delete/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id:Annotated[str, Query(description="Filter key: id")], session: AsyncDB):
    result=await CRUD_todo(session).delete_todo(id)
    if not result:
        raise HTTPException(status_code=404, detail=f"{id} not found")
    return result