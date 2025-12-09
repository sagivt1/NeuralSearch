import pytest
from src.neural import EmbeddingModel, embedder


# The expected dimension of the embedding model being used.
# 'all-MiniLM-L6-v2' produces vectors of length 384.
EXPECTED_DIMENSION = 384


@pytest.fixture(scope="session")
def embedder() -> EmbeddingModel:
    """
    Pytest fixture to provide a single, session-scoped instance of the EmbeddingModel.
    This ensures the model is loaded only once for the entire test session.
    """
    return EmbeddingModel()


def test_embedding_model_is_singleton():
    """
    Verifies that the EmbeddingModel correctly implements the singleton pattern.
    """
    # Creating a new instance should return the same object as the fixture.
    # This confirms only one copy of the heavy model exists in memory.
    another_embedder_instance = EmbeddingModel()
    assert embedder is another_embedder_instance


def test_embed_output_structure_and_type(embedder: EmbeddingModel):
    """
    Checks if the embed method output is a list of floats with the correct dimension.
    """
    embedding = embedder.embed("This is a test sentence.")

    assert isinstance(embedding, list)
    assert len(embedding) == EXPECTED_DIMENSION
    assert all(isinstance(x, float) for x in embedding)


def test_embed_handles_empty_input(embedder: EmbeddingModel):
    """
    Ensures that providing an empty or whitespace-only string results in an empty list.
    """
    # The model should return an empty vector for empty text to avoid downstream errors.
    assert embedder.embed("") == []
    assert embedder.embed("   \t\n  ") == []