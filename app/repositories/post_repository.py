from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.models.post import Post


class PostRepository:

    @staticmethod
    async def create(db: AsyncSession, post: Post):
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(
            select(Post).options(selectinload(Post.votes))
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, post_id):
        result = await db.execute(
            select(Post)
            .options(selectinload(Post.votes))
            .where(Post.id == post_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def delete(db: AsyncSession, post_id):
        await db.execute(delete(Post).where(Post.id == post_id))
        await db.commit()