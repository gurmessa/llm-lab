import pytest

from ...services.metrics.coherence_metric import CoherenceMetric


@pytest.mark.skip(reason="Skipping real coherence tests for now")
class TestCoherenceMetric:
    @pytest.fixture
    def metric(self):
        """CoherenceMetric with default LocalTransformer embeddings."""
        return CoherenceMetric()

    def test_coherent_response(self, metric):
        response = (
            "The water cycle involves evaporation, condensation, and precipitation. "
            "Evaporation occurs when water from oceans, lakes, and rivers turns into vapor. "
            "Condensation happens as the water vapor rises and cools, forming clouds. "
            "Precipitation occurs when water droplets in clouds become heavy and fall as rain or snow. "
            "This cycle is essential for maintaining ecosystems and providing fresh water. "
            "Human activities like deforestation and pollution can disrupt the natural water cycle. "
            "Understanding these processes is crucial for managing water resources sustainably."
        )
        score = metric.compute(response)
        assert 0.4 <= score <= 1.0  # expect high coherence

    def test_incoherent_response(self, metric):
        response = (
            "I woke up early in the morning. "
            "The car is red. "
            "Pineapple tastes good. "
            "I should go jogging now."
        )
        score = metric.compute(response)
        assert 0.0 <= score <= 0.2  # expect low coherence
