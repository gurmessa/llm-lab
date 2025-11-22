import re

import nltk
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize

from .base import Metric
from .constants import CONCLUSION_WORDS, STRUCTURAL_INDICATORS

nltk.download("punkt")  # Download once

# Constants for structural thresholds
MIN_WORDS_FULL = 25
MAX_WORDS_FULL = 400
MIN_WORDS_PARTIAL = 15
MAX_WORDS_PARTIAL = 800
SENTENCE_STD_MIN = 3
SENTENCE_STD_MAX = 15


class StructuralMetric(Metric):
    """
    Structural Quality Metric:
    Evaluates sentence/paragraph variety, structural markers,
    lists, and conclusion indicators.
    """

    def __init__(self):
        self.structural_indicators = STRUCTURAL_INDICATORS
        self.conclusion_words = CONCLUSION_WORDS

    def _get_length_appropriateness_score(self, word_count: int) -> float:
        if MIN_WORDS_FULL <= word_count <= MAX_WORDS_FULL:
            return 1.0
        elif (
            MIN_WORDS_PARTIAL <= word_count < MIN_WORDS_FULL
            or MAX_WORDS_FULL < word_count <= MAX_WORDS_PARTIAL
        ):
            return 0.5
        return 0.0

    def _get_sentence_variety_score(self, sentences: list) -> float:
        if len(sentences) < 2:
            return 0.0
        sentence_lengths = [len(word_tokenize(sent)) for sent in sentences]
        length_std = np.std(sentence_lengths)
        if SENTENCE_STD_MIN <= length_std <= SENTENCE_STD_MAX:
            return 1.0
        return 0.0

    def _get_paragraph_structure_score(self, text: str) -> float:
        paragraph_breaks = text.count("\n\n") + text.count("\n")
        if paragraph_breaks >= 2:
            return 1.0
        elif paragraph_breaks == 1:
            return 0.5
        return 0.0

    def _get_structural_markers_score(self, text: str) -> float:
        structural_count = sum(
            1 for indicator in self.structural_indicators if indicator in text.lower()
        )
        if structural_count >= 1:
            return 1
        return 0.0

    def _get_average_sentence_length_score(self, sentences: list, words: list) -> float:
        if len(sentences) > 0:
            avg_sentence_length = len(words) / len(sentences)
            if 10 <= avg_sentence_length <= 25:
                return 1.0
            elif 8 <= avg_sentence_length <= 30:
                return 0.5
        return 0.0

    def _get_proper_capitalization_score(self, sentences: list) -> float:
        if not sentences:
            return 0.0
        proper_caps = 0
        for sent in sentences:
            sent = sent.lstrip("\"'-•* ")  # remove leading quotes, bullets, dashes
            if sent and sent[0].isupper():
                proper_caps += 1
        return proper_caps / len(sentences)

    def _get_list_enumeration_score(self, text: str, sentences: list) -> float:
        list_indicators = text.count("•") + text.count("- ") + text.count("* ")
        enumeration_patterns = re.findall(r"\b\d+\.\s|\b[a-z]\)\s", text.lower())
        total_items = list_indicators + len(enumeration_patterns)
        if not sentences:
            return 0.0
        return min(total_items / len(sentences), 1.0)

    def _get_conclusion_indicator_score(self, text: str) -> float:
        for word in self.conclusion_words:
            if word in text.lower():
                return 1.0
        return 0.0

    def compute(self, llm_response: str, user_prompt: str = None) -> float:
        """
        Compute a single Structural Quality score (0-1) for an LLM response.
        """
        text = llm_response
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        if len(words) == 0:
            return 0.0

        score = 0.0
        max_score = 8.0  # Total points for all subchecks

        # 1. Length appropriateness
        score += self._get_length_appropriateness_score(len(words))

        # 2. Sentence variety (std of sentence lengths)
        score += self._get_sentence_variety_score(sentences)

        # 3. Paragraph structure
        score += self._get_paragraph_structure_score(text)

        # 4. Structural markers
        score += self._get_structural_markers_score(text)

        # 5. Average sentence length (structural relevance)
        score += self._get_average_sentence_length_score(sentences, words)

        # 6. Proper capitalization
        score += self._get_proper_capitalization_score(sentences)

        # 7. Lists or enumerations
        score += self._get_list_enumeration_score(text, sentences)

        # 8. Conclusion indicators
        score += self._get_conclusion_indicator_score(text)
        # Normalize score to 0-1
        return min(score / max_score, 1.0)
