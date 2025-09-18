
from sqlalchemy import TIMESTAMP, delete, select, update
from database.models import User
from sqlalchemy.ext.asyncio import AsyncSession


class CRUD_users:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    # create user
    async def create_user(self, db_Request: User) -> User:
        self.session.add(userRequest)
        await self.session.commit()
        await self.session.refresh(userRequest)
        return userRequest

    # search by key and value for dynamic filter for first value only
    async def get_user_by_key_pk(self, db:User, key: str, value: str):
        column = getattr(User, key, None)
        if column is None:
            raise ValueError(f"Invalid column name: {key}")
        stmt = select(User).where(column == value)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    
    async def update_users(self, id: str, key: str, value: str):
        column = getattr(User, key, None)
        stmt = update(User).where(User.id == id).values({column: value}).returning(User)
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.mappings().first()
        return dict(row) if row else None
 

    async def delete_todo(self, id: str) -> bool:
        stmt = select(User).where(User.id == id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return {"deleted":id}
