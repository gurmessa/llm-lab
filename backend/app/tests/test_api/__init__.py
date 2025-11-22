from unittest.mock import MagicMock

import pytest

from app.db.enums import ExperimentStatus, ResponseStatus
from app.db.models.experiment_models import Experiment, ExperimentRun, ResponseRecord
from app.services.core.experiment_orchestrator import ExperimentOrchestrator


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    # Make commit and query safe to call
    session.commit = MagicMock()
    session.query = MagicMock()
    return session


def test_run_experiment_completes_successfully(mock_db_session):
    # Mock experiment with one run
    run = ExperimentRun(id=1, temperature=0.7, top_p=0.9, max_output_tokens=100)
    experiment = Experiment(
        id=1,
        user_prompt="Hello",
        model_name="test-model",
        runs=[run],
        status=ExperimentStatus.PENDING,
    )

    # Mock query to return no existing responses
    mock_db_session.query().filter().order_by().first.return_value = None
    mock_db_session.query().filter().all.return_value = []

    # Patch ExperimentRunner inside the orchestrator
    orchestrator = ExperimentOrchestrator(experiment, mock_db_session)
    orchestrator.runner.run = MagicMock(
        return_value={
            "llm_response": "This is a test response.",
            "metrics": {"accuracy": 1.0},
        }
    )

    # Run the experiment
    result_experiment = orchestrator.run_experiment()

    # Assertions
    assert result_experiment.status == ExperimentStatus.COMPLETED
    # Check that runner was called
    orchestrator.runner.run.assert_called_once_with(
        user_prompt="Hello", temperature=0.7, top_p=0.9, max_tokens=100
    )
    # Ensure commit was called at least once
    assert mock_db_session.commit.called
