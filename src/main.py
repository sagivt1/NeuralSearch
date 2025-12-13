from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config import get_settings
from src.database import init_db, get_session
from src.models import Document
from src.schemas import DocumentResponse
from src.tasks import process_document


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
def create_app() -> FastAPI:
    setting = get_settings()

    app = FastAPI(
        title=setting.APP_NAME,
        # The lifespan context manager handles startup/shutdown logic.
        lifespan=lifespan,
    )
    
    return app

app = create_app()

@app.get("/")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    """

    """

    try:
        content = await file.read()
        text_content = content.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a UTF-8 text file.")
    

    # save to database
    new_doc = Document(filename=file.filename, content=text_content)
    session.add(new_doc)
    await session.commit()
    await session.refresh(new_doc)

    # Trigger Background task 
    # Pass the ID so the worker know whice DB row to update
    process_document.delay(new_doc.filename, new_doc.content)

    return new_doc

@app.get("/documents", response_model=list[DocumentResponse])
async def list_documents(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Document))
    documents = result.scalars().all()
    return documents


