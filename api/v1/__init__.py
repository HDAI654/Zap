from .endpoints.auth import router as auth_router
from .endpoints.user import router as user_router
from .endpoints.voice import router as voice_router

routers = {
    "auth": auth_router,
    "user": user_router,
    "voice": voice_router,
}
