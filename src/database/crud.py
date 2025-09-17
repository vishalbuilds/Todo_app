from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import TIMESTAMP, delete, select, update
from database.models import List
from sqlalchemy.ext.asyncio import AsyncSession

class CRUD_items:
    def __init__(self,session: AsyncSession):
        self.session: AsyncSession = session

    #create row 
    async def add_todo(self, id:str, title:str, description:str, status:str, priority: str, tags:dict, due_date:TIMESTAMP, user_id:str=None):

        stmt=insert(List).values( id=id, title=title, description=description, status=status, priority=priority, tags=tags, due_date=due_date, user_id=user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    # search by key and value for dynamic filter for first value only
    async def get_todo_by_key_pk(self,key: str, value:str):

        column = getattr(List, key, None)
        if column is None:
            raise ValueError(f"Invalid column name: {key}")
        stmt=select(List).where(column == value)
        result=await self.session.execute(stmt)
        return result.scalars().first()

    # search by key and value for dynamic filter for maltiple values
    async def get_todo_by_key_many_pk(self,key: str, value:str):

        column = getattr(List, key, None)
        if column is None:
            raise ValueError(f"Invalid column name: {key}")
        stmt=select(List).where(column == value)
        result=await self.session.execute(stmt)
        return result.scalars().all()


    async def update_todo(self,id:str,priority:str):
        stmt=update(List).values(priority=priority).where(List.id==id)
        print(stmt)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_todo(self, id:str):
        stmt=delete(List).where(List.id==id)
        print(stmt)
        await self.session.execute(stmt)
        await self.session.commit()


 
