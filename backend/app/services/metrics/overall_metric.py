from .base import Metric
from .coherence_metric import CoherenceMetric
from .structural_metric import StructuralMetric

METRIC_CLASSES = {
    "coherence": CoherenceMetric,
    "structure": StructuralMetric,
}

METRIC_WEIGHTS = {
    "coherence": 1,
    "structure": 1,
}


class OverallMetric(Metric):
    """
    Aggregates multiple metrics into a weighted overall score.
    Returns individual scores and overall score as a dictionary.
    """

    def __init__(self, selected_metrics: list = None):
        if not selected_metrics:
            selected_metrics = list(METRIC_CLASSES.keys())
        else:
            selected_metrics = [m for m in selected_metrics if m in METRIC_CLASSES]

        self.metrics = {
            name: METRIC_CLASSES[name]()
            for name in selected_metrics
            if name in METRIC_CLASSES
        }

    def compute(self, llm_response: str, user_prompt: str = None) -> dict:
        results = {}
        weighted_sum = 0
        total_weight = 0

        for name, metric in self.metrics.items():
            score = metric.compute(llm_response, user_prompt)
            results[name] = score
            weight = METRIC_WEIGHTS.get(name, 1.0)  # default weight = 1
            weighted_sum += score * weight
            total_weight += weight

        overall_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        results["overall"] = overall_score
        return results
