import os
from typing import List

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from .base import EmbeddingProvider

load_dotenv()


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """
    Embedding provider using OpenAI API.
    """

    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def embed(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts using OpenAI API.
        Returns a numpy array of shape (len(texts), embedding_dim)
        """
        if not texts:
            return np.array([])

        response = self.client.embeddings.create(model=self.model_name, input=texts)
        embeddings = [item.embedding for item in response.data]
        return np.array(embeddings)
