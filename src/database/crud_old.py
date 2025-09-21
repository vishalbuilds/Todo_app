
from ast import Dict
from sqlalchemy import TIMESTAMP, delete, select, update
from database.models import  User,List, User_sessions
from sqlalchemy.ext.asyncio import AsyncSession


type DB_TYPE= List | User | User_sessions

class CRUD:
    def __init__(self,db_name:DB_TYPE, session: AsyncSession) -> DB_TYPE:
        self.session: AsyncSession = session
        self.db_name=db_name

    # create entry by Table type request
    async def create_unique(self, _Request ):
        self.session.add(_Request)
        await self.session.commit()
        await self.session.refresh(_Request)
        return _Request

    # search by key and value for dynamic filter for unqie both pk
    async def get_by_id_pk_unqie_return(self, key: str, value: str) -> DB_TYPE:

        column = getattr(self.db_name,key,None)
        if column is None:
            raise ValueError(f"Invalid column name: {key}")
        stmt = select(self.db_name).where(column == value)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    # search by key and value for dynamic filter for only unique id pk with multiple value for other pk
    async def get_by_id_pk_Multiple_return(self, key: str, value: str) -> DB_TYPE:

        column = getattr(self.db_name,key,None)
        if column is None:
            raise ValueError(f"Invalid column name: {key}")
        stmt = select(self.db_name).where(column == value)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    


    
    #update by id to update column "key" with "value"
    async def update_by_id(self, id: str, key: str, value: str) -> Dict | None:
        column = getattr(self.db_name, key, None)
        stmt = update(self.db_name).where(self.db_name.id == id).values({key: value}).returning(self.db_name) # .values({column: value})
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.mappings().first()
        return dict(row) if row else None
 
    #delete by id 
    async def delete_by_id(self, id: str) -> Dict:
        stmt = select(self.db_name).where(self.db_name.id == id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return {"deleted":id}
