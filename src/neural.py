import torch
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    """
    Singleton class to manage a single instance of the SentenceTransformer model.
    Prevents re-loading the heavy model into memory across the application.
    """
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingModel, cls).__new__(cls)
            
            # Auto-select best available device for hardware acceleration.
            # Prioritizes CUDA, then Apple Silicon (MPS), falling back to CPU.
            device = "cpu"
            if torch.cuda.is_available():
                device = "cuda"
                print(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
            elif torch.backends.mps.is_available():
                device = "mps"
                print("AI Model loading on Apple Silicon (MPS)")
            else:
                print("AI Model loading on CPU")
            
            # Pass the selected device to the model for performance gains.
            cls._model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
        return cls._instance
    
    def embed(self, text: str) -> list[float]:
        """Generates a vector embedding for a given text string."""
        # Return an empty vector for empty/whitespace input to prevent downstream errors.
        if not text.strip():
            return []
        
        embedding = self._model.encode(text)
        return embedding.tolist()

# Global singleton instance.
# Import this object in other modules to use the embedding model.
embedder = EmbeddingModel()


    
           