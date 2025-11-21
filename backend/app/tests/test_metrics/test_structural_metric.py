import pytest
from nltk.tokenize import sent_tokenize, word_tokenize

from app.services.metrics.structural_metric import StructuralMetric


@pytest.fixture
def metric():
    return StructuralMetric()


# Test the sub-metrics


def test_length_appropriateness(metric):
    short_text = "Short text."  # < MIN_WORDS_PARTIAL
    long_text = "Word " * 30  # between MIN_WORDS_FULL and MAX_WORDS_FULL
    too_long_text = "Word " * 500  # > MAX_WORDS_PARTIAL

    assert (
        metric._get_length_appropriateness_score(len(word_tokenize(short_text))) == 0.0
    )
    assert (
        metric._get_length_appropriateness_score(len(word_tokenize(long_text))) == 1.0
    )
    assert (
        metric._get_length_appropriateness_score(len(word_tokenize(too_long_text)))
        == 0.5
    )


def test_sentence_variety(metric):
    short_sents = ["Hello.", "Hi."]  # very similar
    varied_sents = ["This is short.", "This is a much longer sentence to test variety."]

    assert metric._get_sentence_variety_score(short_sents) == 0.0
    assert metric._get_sentence_variety_score(varied_sents) == 1.0


def test_paragraph_structure(metric):
    text_no_breaks = "Sentence one. Sentence two."
    text_one_break = "Sentence one.\nSentence two."
    text_two_breaks = "Para one.\n\nPara two."

    assert metric._get_paragraph_structure_score(text_no_breaks) == 0.0
    assert metric._get_paragraph_structure_score(text_one_break) == 0.5
    assert metric._get_paragraph_structure_score(text_two_breaks) == 1.0


def test_structural_markers(metric):
    text_with_markers = "First, we do this. Then we do that."
    text_without_markers = "We do this and then that."

    assert metric._get_structural_markers_score(text_with_markers) == 1.0
    assert metric._get_structural_markers_score(text_without_markers) == 0.0


def test_average_sentence_length(metric):
    text = (
        "This sentence is deliberately long to reach the threshold for scoring. "
        "Here is another long sentence that ensures the average sentence length is sufficient."
    )
    sents = sent_tokenize(text)
    words = word_tokenize(text)

    score = metric._get_average_sentence_length_score(sents, words)
    assert score == 1.0


def test_proper_capitalization(metric):
    sents = ["Hello world.", "This is fine."]
    sents_bad = ["hello world.", "this is bad."]

    assert metric._get_proper_capitalization_score(sents) == 1.0
    assert metric._get_proper_capitalization_score(sents_bad) == 0.0


def test_list_enumeration(metric):
    text_with_list = "• Item one\n• Item two\n1. Numbered item"
    sents = sent_tokenize("This is a sentence.")
    score = metric._get_list_enumeration_score(text_with_list, sents)
    assert 0.0 < score <= 1.0

    text_without_list = "Just plain text."
    score2 = metric._get_list_enumeration_score(text_without_list, sents)
    assert score2 == 0.0


def test_conclusion_indicator(metric):
    text_with_conclusion = "In conclusion, we achieved our goal."
    text_without_conclusion = "This is a normal sentence."

    assert metric._get_conclusion_indicator_score(text_with_conclusion) == 1.0
    assert metric._get_conclusion_indicator_score(text_without_conclusion) == 0.0


# Test combined compute


def test_empty_response(metric):
    llm_response = ""
    score = metric.compute(llm_response)
    assert score == 0.0


def test_short_response(metric):
    llm_response = "Hello."
    score = metric.compute(llm_response)
    assert 0.0 <= score <= 0.5


def test_well_structured_response(metric):
    llm_response = (
        "First, we will analyze the data. "
        "Then, we will summarize our findings. "
        "Finally, in conclusion, the results show significant improvement.\n\n"
        "• Item one\n"
        "• Item two\n"
        "• Item three"
    )
    score = metric.compute(llm_response)
    assert 0.7 <= score <= 1.0


def test_response_without_structural_markers(metric):
    llm_response = (
        "We will analyze the data carefully over the next few days. "
        "The results are interesting and may provide useful insights for the team. "
        "This process should help us make better decisions based on the available information."
    )
    score = metric.compute(llm_response)
    # Medium score expected because no structural markers
    assert 0.3 <= score <= 0.7


def test_response_with_long_sentences(metric):
    llm_response = (
        "We will analyze the data carefully over the next few days. "
        "The results are interesting and may provide useful insights for the team. "
        "This process should help us make better decisions based on the available information."
    )
    score = metric.compute(llm_response)
    assert 0.0 <= score <= 0.7
