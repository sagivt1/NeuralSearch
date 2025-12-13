from src.worker import celery_app

@celery_app.task(name="process_document")
def process_document(filename: str, text: str):
    """
    Take text and covert it for vector then print the vector
    """
    from src.neural import embedder

    print(f"Processing file: {filename}")

    vector = embedder.embed(text)

    print(f"Embedding complete. vector length {len(vector)}")
    return {"filename": filename, "status" : "done"}