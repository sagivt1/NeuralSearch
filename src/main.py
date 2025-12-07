from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting up {get_settings().APP_NAME}...")
    yield
    print(f"Shutting down...")

def create_app():
    setting = get_settings()
    
    app = FastAPI(
        title=setting.APP_NAME,
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health_check():
        return {
            "status" : "healthy",
            "environment" : setting.ENVIRONMENT,
            "version" : "1.0.0"
        }
    
    return app

app = create_app()