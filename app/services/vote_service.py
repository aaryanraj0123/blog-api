from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.vote_repository import VoteRepository
from app.repositories.post_repository import PostRepository
from app.models.vote import Vote


class VoteService:
    
    @staticmethod
    async def vote(db: AsyncSession, user, post_id, vote_value: int):

        # ensure post exists
        post = await PostRepository.get_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found",)
        existing_vote = await VoteRepository.get_vote(db, user.id, post_id)

        # ADD VOTE
        if vote_value == 1:
            if existing_vote:
                raise HTTPException(status_code=409, detail="Already voted",)
            
            vote = Vote(
                user_id=user.id,
                post_id=post_id,
            )

            await VoteRepository.create_vote(db, vote)

            return {"message": "Vote added"}
        
        # REMOVE VOTE
        else:
            if not existing_vote:
                raise HTTPException(status_code=404, detail="Vote does not exist",)
            
            await VoteRepository.delete_vote(db, user.id, post_id)

            return {"message": "Vote removed"}