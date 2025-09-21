from typing import Type, TypeVar, Any, Dict, List as TypingList, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)

class GenericCRUD:
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    # Create a new record
    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    # Get one record by multiple filters
    async def get_one(self, filters: Dict[str, Any]) -> Optional[T]:
        stmt = select(self.model)
        for key, value in filters.items():
            column = getattr(self.model, key, None)
            if column is None:
                raise ValueError(f"Invalid column name: {key}")
            stmt = stmt.where(column == value)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    # Get all records by multiple filters
    async def get_all(self, filters: Dict[str, Any]) -> TypingList[T]:
        stmt = select(self.model)
        for key, value in filters.items():
            column = getattr(self.model, key, None)
            if column is None:
                raise ValueError(f"Invalid column name: {key}")
            stmt = stmt.where(column == value)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # Update record(s) by filters
    async def update(self, filters: Dict[str, Any], values: Dict[str, Any]) -> Optional[Dict]:
        stmt = update(self.model)
        for key, value in filters.items():
            column = getattr(self.model, key, None)
            if column is None:
                raise ValueError(f"Invalid filter column: {key}")
            stmt = stmt.where(column == value)
        stmt = stmt.values(**values).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        row = result.mappings().first()
        return dict(row) if row else None

    # Delete record(s) by filters
    async def delete(self, filters: Dict[str, Any]) -> bool:
        stmt = select(self.model)
        for key, value in filters.items():
            column = getattr(self.model, key, None)
            if column is None:
                raise ValueError(f"Invalid column name: {key}")
            stmt = stmt.where(column == value)
        result = await self.session.execute(stmt)
        obj = result.scalars().first()
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
