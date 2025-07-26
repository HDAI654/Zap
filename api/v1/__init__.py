from .endpoints.auth import router as auth_router
from .endpoints.user import router as user_router

routers = {
    "auth": auth_router,
    "user": user_router,
}
