from fastapi import FastAPI
from api import v1
from db.base import Base
from db.session import engine
from middleware.cors import add_cors_middleware
from fastapi.responses import FileResponse
from core.config import settings

app = FastAPI(title="Zap - AI Accounting Platform")
add_cors_middleware(app)


# simple panel page
@app.get("/simple-panel")
def panel_page():
    return FileResponse("./simple_panel.html")


@app.get("/")
async def root():
    return {"message": "Welcome to Zap!"}

app.include_router(v1.routers["auth"], prefix=f"/api/v{settings.API_ACTIVE_VERSION}/auth", tags=["auth"])
app.include_router(v1.routers["user"], prefix=f"/api/v{settings.API_ACTIVE_VERSION}/user", tags=["user"])
app.include_router(v1.routers["voice"], prefix=f"/api/v{settings.API_ACTIVE_VERSION}/voice", tags=["voice"])
#app.include_router(v1.routers["query"], prefix=f"/api/v{settings.API_ACTIVE_VERSION}/query", tags=["query"])
#app.include_router(v1.routers["tables"], prefix=f"/api/v{settings.API_ACTIVE_VERSION}/tables", tags=["tables"])



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    #logger.info("Server Started.")
