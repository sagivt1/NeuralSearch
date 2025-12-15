from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from src.config import get_settings
from src.database import init_db, get_session
from src.models import Document
from src.schemas import DocumentResponse
from src.tasks import process_document
from src.schemas import SearchResponse
from src.neural import embedder

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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

app = create_app()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    """
    Accepts a file upload, saves its content to the database,
    and triggers a background task to generate its vector embedding.
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

    # Offload the CPU-intensive embedding generation to a background worker.
    process_document.delay(new_doc.id)

    return new_doc

@app.get("/documents", response_model=list[DocumentResponse])
async def list_documents(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Document))
    documents = result.scalars().all()
    return documents

@app.post("/search", response_model=list[SearchResponse])
async def search_documents(query: str, session: AsyncSession = Depends(get_session)):
    """
    Searches for documents semantically similar to the query.
    1. Converts the query text into a vector embedding.
    2. Performs a nearest neighbor search in the database.
    """

    # Embedding generation is CPU-bound, run in a thread pool to avoid blocking the event loop.
    query_vector = await run_in_threadpool(embedder.embed, query)


    # Use the L2 distance operator (<->) from pgvector to find the nearest neighbors.
    # The `l2_distance` method is a SQLAlchemy-friendly wrapper for this operator.
    statement = select(Document).order_by(Document.embedding.l2_distance(query_vector)).limit(5)

    result = await session.execute(statement)
    documents = result.scalars().all()

    return documents

    
