from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config import get_settings
from src.database import init_db


# Manages application startup and shutdown events.
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting up {get_settings().APP_NAME}...")
    # Initialize the database and create tables before the app starts receiving requests.
    await init_db()
    yield
    print(f"Shutting down...")

# Application factory pattern.
# Makes it easier to configure and test the application.
def create_app():
    setting = get_settings()

    
    app = FastAPI(
        title=setting.APP_NAME,
        # The lifespan context manager handles startup/shutdown logic.
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
