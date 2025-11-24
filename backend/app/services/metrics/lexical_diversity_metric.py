from nltk.tokenize import word_tokenize

from .base import Metric


class LexicalDiversityMetric(Metric):
    """
    Computes lexical diversity of the LLM response.
    Returns a float between 0 (low diversity) and 1 (high diversity).
    """

    def compute(self, llm_response: str, user_prompt: str = None) -> float:
        """
        Compute lexical diversity score for the LLM response.
        """
        if not llm_response:
            return 0.0

        # Tokenize text into words
        tokens = word_tokenize(llm_response.lower())  # lowercase for consistency
        if not tokens:
            return 0.0

        # Remove punctuation tokens
        words = [t for t in tokens if t.isalpha()]

        # Compute lexical diversity
        return len(set(words)) / len(words) if words else 0.0
