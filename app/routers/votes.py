from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.vote import VoteRequest
from app.services.vote_service import VoteService
from app.core.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("")
async def vote(
    data: VoteRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await VoteService.vote(
        db,
        user,
        data.post_id,
        data.vote,
    ) 