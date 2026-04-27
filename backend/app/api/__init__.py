from app.api.auth.router import router as auth_router
from app.api.admin.router import router as admin_router
from app.api.deliver.router import router as deliver_router
from app.api.member.router import router as member_router
from app.api.older.router import router as older_router

__all__ = [
    "auth_router",
    "admin_router", 
    "deliver_router",
    "member_router",
    "older_router"
]