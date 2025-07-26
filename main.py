from fastapi import FastAPI
from api import v1
from db.base import Base
from db.session import engine
from middleware.cors import add_cors_middleware
from fastapi.responses import FileResponse
from core.config import settings

app = FastAPI(title="Zap - AI Accounting Platform")
add_cors_middleware(app)


# simple login page
@app.get("/login-page")
def login_page():
    return FileResponse("./login_register.html")


@app.get("/")
async def root():
    return {"message": "Welcome to Zap!"}

app.include_router(v1.routers["auth"], prefix=f"/api/v{settings.API_ACTIVE_VERSION}/auth", tags=["auth"])
app.include_router(v1.routers["user"], prefix=f"/api/v{settings.API_ACTIVE_VERSION}/users", tags=["users"])
#app.include_router(v1.routers["voice"].router, prefix=f"/api/v{settings.API_ACTIVE_VERSION}/voice", tags=["voice"])
#app.include_router(v1.routers["query"].router, prefix=f"/api/v{settings.API_ACTIVE_VERSION}/query", tags=["query"])
#app.include_router(v1.routers["tables"].router, prefix=f"/api/v{settings.API_ACTIVE_VERSION}/tables", tags=["tables"])



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    #logger.info("Server Started.")
