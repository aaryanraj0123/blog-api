from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.vote import Vote 
class VoteRepository:

    @staticmethod 
    async def get_vote(db: AsyncSession, user_id, post_id):
        result = await db.execute(
            select(Vote).where(
                Vote.user_id == user_id,
                Vote.post_id == post_id,
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_vote(db: AsyncSession, vote: Vote):
        db.add(vote)
        await db.commit()

    @staticmethod
    async def delete_vote(db: AsyncSession, user_id, post_id):
        await db.execute(
            delete(Vote).where(
                Vote.user_id == user_id,
                Vote.post_id == post_id,
            )
        )
        await db.commit()