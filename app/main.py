from fastapi import FastAPI, Depends
from app.routers import auth
from app.dependencies.auth import get_current_user, require_role
from app.routers import posts
from app.routers import votes

app = FastAPI(title="Blog API")

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(votes.router)

@app.get("/me")
async def get_me(user=Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email,
        "role": user.role.value,
    }

@app.get("/admin-only")
async def admin_only(user=Depends(require_role("ADMIN"))):
    return {"message": "Welcome admin"}

@app.get("/health")
async def health():
    return {"status": "OK"}