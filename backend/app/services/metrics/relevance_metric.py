import numpy as np

from ..embedding.openai_embedding import OpenAIEmbeddingProvider
from .base import Metric


class RelevanceMetric(Metric):
    """
    Computes relevance between a user prompt and LLM response using embeddings.
    Returns a score between 0 and 1 (can be converted to percentage).
    """

    def __init__(self):
        self.embedding_provider = OpenAIEmbeddingProvider()

    @staticmethod
    def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors and normalize to 0-1."""
        if vec1.size == 0 or vec2.size == 0:
            return 0.0
        cos_sim = float(
            np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        )
        # Normalize to 0-1
        return (cos_sim + 1) / 2

    def compute(self, llm_response: str, user_prompt: str = None) -> float:
        """
        Compute relevance score between prompt and LLM response.
        Returns a float between 0 (unrelated) and 1 (highly relevant).
        """
        if not user_prompt or not llm_response:
            return 0.0

        embeddings = self.embedding_provider.embed([user_prompt, llm_response])
        prompt_emb, response_emb = embeddings[0], embeddings[1]
        return self._cosine_similarity(prompt_emb, response_emb)
