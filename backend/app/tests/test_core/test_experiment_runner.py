# test_experiment_runner.py
from unittest.mock import MagicMock, patch

import pytest

from app.services.core.experiment_runner import ExperimentRunner
from app.services.llm.constants import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
)


def test_experiment_runner_run():
    user_prompt = "Hello, LLM!"

    # Mock OpenAIResponder.run to return a fixed response
    with patch("app.services.core.experiment_runner.OpenAIResponder") as MockResponder:
        mock_responder_instance = MockResponder.return_value
        mock_responder_instance.run.return_value = "mocked response"

        # Mock OverallMetric.compute to return a fixed score
        with patch("app.services.core.experiment_runner.OverallMetric") as MockMetric:
            mock_metric_instance = MockMetric.return_value
            mock_metric_instance.compute.return_value = {"score": 1.0}

            runner = ExperimentRunner()
            result = runner.run(user_prompt)

            # Assertions
            assert result["llm_response"] == "mocked response"
            assert result["metrics"] == {"score": 1.0}

            # Ensure mocks were called with correct arguments
            mock_responder_instance.run.assert_called_once_with(
                user_prompt,
                temperature=DEFAULT_TEMPERATURE,
                top_p=DEFAULT_TOP_P,
                max_tokens=DEFAULT_MAX_TOKENS,
            )
            mock_metric_instance.compute.assert_called_once_with("mocked response")
