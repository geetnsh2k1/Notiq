from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.sql import func
from sqlalchemy.inspection import inspect


Base = declarative_base()


class BaseModel(Base, AsyncAttrs):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    async def save(self, session: AsyncSession):
        """
        Asynchronously saves the instance to the DB.

        Args:
            session (AsyncSession): SQLAlchemy async session
        """
        try:
            session.add(self)
            await session.flush()
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

    def to_dict(self) -> dict:
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }