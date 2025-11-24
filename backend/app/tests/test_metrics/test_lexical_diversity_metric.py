import pytest

from ...services.metrics.lexical_diversity_metric import LexicalDiversityMetric


@pytest.fixture
def metric():
    return LexicalDiversityMetric()


def test_diverse_llm_response(metric):
    llm_response_diverse = """
    Artificial intelligence, or AI, encompasses a wide range of techniques 
    including machine learning, deep learning, natural language processing, 
    and computer vision. Each method has its own strengths, limitations, 
    and ideal applications across industries such as healthcare, finance, 
    and transportation.
    """
    score = metric.compute(llm_response_diverse)
    # Diverse text should have a higher score
    assert score > 0.6


def test_non_diverse_llm_response(metric):
    llm_response_nondense = """
    AI is AI is AI is AI. Machine learning is machine learning is machine learning. 
    Deep learning is deep learning is deep learning.
    """
    score = metric.compute(llm_response_nondense)
    # Non-diverse text should have a lower score
    assert score < 0.3
