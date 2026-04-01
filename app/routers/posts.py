from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services.post_service import PostService
from app.core.database import get_db
from app.dependencies.auth import require_role, get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

# CREATE POST
@router.post("", response_model=PostResponse)
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role("AUTHOR", "ADMIN")),
):
    return await PostService.create_post(db, data.title, data.content, user)

# GET ALL POSTS
@router.get("", response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    return await PostService.get_posts(db)

# GET SINGLE POST
@router.get("/{id}", response_model=PostResponse)
async def get_post(id: UUID, db: AsyncSession = Depends(get_db)):
    return await PostService.get_post(db, id)

# UPDATE POST
@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: UUID,  
    data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await PostService.update_post(db, post_id, data, user)

# DELETE POST
@router.delete("/{post_id}")
async def delete_post(
    post_id: UUID, 
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await PostService.delete_post(db, post_id, user)