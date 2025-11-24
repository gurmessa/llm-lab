import pytest

from ...services.metrics.relevance_metric import RelevanceMetric


@pytest.fixture
def metric():
    return RelevanceMetric()


@pytest.mark.skip(reason="tested already once")
class TestRelevanceMetric:
    def test_identical_texts(metric):
        prompt = "How do I cook sweet potatoes?"
        response = "How do I cook sweet potatoes?"
        score = metric.compute(response, prompt)
        print(f"Identical texts: {score*100:.2f}%")
        assert score > 0.99  # should be very close to 1

    def test_related_texts(metric):
        prompt = "How do I cook sweet potatoes?"
        response = "You can bake sweet potatoes in the oven at 200°C for 45 minutes."
        score = metric.compute(response, prompt)
        print(f"Related texts: {score*100:.2f}%")
        assert score > 0.8  # moderately high

    def test_unrelated_texts(metric):
        prompt = "How do I cook sweet potatoes?"
        response = "The weather today is sunny with clear skies."
        score = metric.compute(response, prompt)
        print(f"Unrelated texts: {score*100:.2f}%")
        assert score < 0.6  # should be low

    def test_empty_response(metric):
        prompt = "How do I cook sweet potatoes?"
        response = ""
        score = metric.compute(response, prompt)
        print(f"Empty response: {score*100:.2f}%")
        assert score == 0.0

    def test_empty_prompt(metric):
        prompt = ""
        response = "You can bake sweet potatoes in the oven."
        score = metric.compute(response, prompt)
        print(f"Empty prompt: {score*100:.2f}%")
        assert score == 0.0
