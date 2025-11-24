from unittest.mock import patch

import pytest

from ...services.metrics.coherence_metric import CoherenceMetric
from ...services.metrics.overall_metric import OverallMetric
from ...services.metrics.relevance_metric import RelevanceMetric
from ...services.metrics.structural_metric import StructuralMetric


def test_overall_metric_returns_dict():
    # Mock compute methods for CoherenceMetric and StructuralMetric
    with patch.object(CoherenceMetric, "compute", return_value=0.9), patch.object(
        StructuralMetric, "compute", return_value=0.8
    ), patch.object(RelevanceMetric, "compute", return_value=0.85):

        overall = OverallMetric()
        result = overall.compute(
            llm_response="Sample response", user_prompt="Sample prompt"
        )

        # Check result is a dictionary
        assert isinstance(result, dict)

        # Check it has the correct keys
        assert "coherence" in result
        assert "structure" in result
        assert "relevance" in result
        assert "overall" in result

        # Check the overall score is correct weighted average
        # Here both weights are 1, so average = (0.9 + 0.8 + 0.85)/3 = 0.85
        assert result["overall"] == pytest.approx(0.85)
