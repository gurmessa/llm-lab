import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity

from ..embedding.openai_embedding import OpenAIEmbeddingProvider
from .base import Metric


class CoherenceMetric(Metric):
    def __init__(self):
        self.embedding_provider = OpenAIEmbeddingProvider()

    def compute(self, llm_response: str, user_prompt: str = None) -> float:
        """
        Compute coherence score for an LLM response.
        """
        sentences = sent_tokenize(llm_response)
        if not sentences:
            return 0.0  # empty response

        if len(sentences) == 1:
            return 1.0  # single sentence fully coherent

        embeddings = self.embedding_provider.embed(sentences)
        sim_scores = [
            cosine_similarity([embeddings[i]], [embeddings[i + 1]])[0][0]
            for i in range(len(embeddings) - 1)
        ]
        final_score = float(np.mean(sim_scores))

        final_score = max(0.0, min(1.0, final_score))
        """
        # Simple linear scaling based on observed min/max
        min_raw = 0.1   # empirically determined for incoherent text
        max_raw = 0.5   # empirically determined for coherent text
        scaled_score = (final_score - min_raw) / (max_raw - min_raw)  # scale 0-1
        scaled_score = max(0, min(1, scaled_score))  # clamp to [0,1]
        percentage = int(scaled_score * 100)
        """
        return final_score
