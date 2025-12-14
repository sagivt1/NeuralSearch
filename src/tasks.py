from sqlmodel import Session, select
from src.worker import celery_app
from src.database import get_sync_engine
from src.models import Document

# Use a synchronous database engine for the Celery worker.
# Workers run in a separate process and don't share the FastAPI async event loop.
sync_engine = get_sync_engine()


@celery_app.task(name="process_document")
def process_document(doc_id: int):
    """
    Background task to generate and save a vector embedding for a document.
    Triggered after a new document is uploaded.
    """
    # Lazy import the embedding model inside the task.
    # Avoids loading the heavy model into the main worker process's memory
    # until this specific task is executed.
    from src.neural import embedder
    
    with Session(sync_engine) as session:
        doc = session.get(Document, doc_id)

        # Gracefully handle cases where the document might be deleted
        # between the task being queued and its execution.
        if not doc:
            print(f"Document {doc_id} not found, skipping processing.")
            return
       
        print(f"Processing file: {doc.filename}")
        vector = embedder.embed(doc.content)

        doc.embedding = vector
        session.add(doc)
        session.commit()

        print(f"Saved embedding for doc {doc_id}. Vector len: {len(vector)}")
        return {"id": doc_id, "status": "Processed"}