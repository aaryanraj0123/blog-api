from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from datetime import datetime

from app.models.post import Post
from app.repositories.post_repository import PostRepository


class PostService:
    @staticmethod
    async def create_post(db: AsyncSession, title: str, content: str, user):
        post = Post(
            title=title,
            content=content,
            author_id=user.id,
        )

        await PostRepository.create(db, post)

        result = await db.execute(
            select(Post).options(selectinload(Post.votes)).where(Post.id == post.id)
        )
        post = result.scalar_one()

        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "votes": len(post.votes),
        }

    @staticmethod
    async def get_posts(db: AsyncSession):
        result = await db.execute(select(Post).options(selectinload(Post.votes)))
        posts = result.scalars().all()

        return [
            {
                "id": p.id,
                "title": p.title,
                "content": p.content,
                "author_id": p.author_id,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
                "votes": len(p.votes),
            }
            for p in posts
        ]

    @staticmethod
    async def get_post(db: AsyncSession, post_id):
        result = await db.execute(
            select(Post).options(selectinload(Post.votes)).where(Post.id == post_id)
        )

        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )

        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "votes": len(post.votes),
        }

    @staticmethod
    async def update_post(db: AsyncSession, post_id, data, user):
        post = await PostRepository.get_by_id(db, post_id)

        if not post:
            raise HTTPException(
                status_code=404,
                detail="Post not found",
            )

        if user.role.value != "ADMIN" and post.author_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to update this post",
            )

        if data.title is not None:
            post.title = data.title

        if data.content is not None:
            post.content = data.content

        post.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(post)

        result = await db.execute(
            select(Post).options(selectinload(Post.votes)).where(Post.id == post.id)
        )
        post = result.scalar_one()

        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "votes": len(post.votes),
        }

    @staticmethod
    async def delete_post(db: AsyncSession, post_id, user):
        post = await PostRepository.get_by_id(db, post_id)

        if not post:
            raise HTTPException(
                status_code=404,
                detail="Post not found",
            )

        if user.role.value != "ADMIN":
            raise HTTPException(
                status_code=403,
                detail="Only admin can delete posts",
            )

        await PostRepository.delete(db, post_id)

        return {"message": "Post deleted successfully"}
