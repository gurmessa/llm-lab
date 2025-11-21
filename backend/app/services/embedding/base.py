from abc import ABC, abstractmethod

import numpy as np


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> np.ndarray:
        """Return embeddings for a list of texts"""
        pass
