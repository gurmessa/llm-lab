from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.enums import ExperimentStatus, ResponseStatus
from app.db.models.experiment_models import Experiment, ExperimentRun, ResponseRecord
from app.services.core.experiment_orchestrator import ExperimentOrchestrator
from app.services.llm.constants import DEFAULT_OPENAI_MODEL_NAME


@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def experiment_with_runs():
    run1 = ExperimentRun(id=1, temperature=0.7, top_p=0.9, max_output_tokens=100)
    run2 = ExperimentRun(id=2, temperature=0.8, top_p=0.85, max_output_tokens=150)
    experiment = Experiment(
        id=1,
        user_prompt="Hello world",
        model_name=DEFAULT_OPENAI_MODEL_NAME,
        runs=[run1, run2],
        status=ExperimentStatus.PENDING,
    )
    return experiment


def test_all_runs_success(experiment_with_runs, test_db):
    orchestrator = ExperimentOrchestrator(experiment_with_runs, test_db)

    # Mock the runner to always succeed
    orchestrator.runner.run = MagicMock(
        return_value={
            "llm_response": "This is a test response.",
            "metrics": {"accuracy": 1.0},
        }
    )

    result_experiment = orchestrator.run_experiment()

    # Assert experiment is completed
    assert result_experiment.status == ExperimentStatus.COMPLETED

    # Check that ResponseRecords were created in DB
    responses = test_db.query(ResponseRecord).all()
    assert len(responses) == 2
    for r in responses:
        assert r.status == ResponseStatus.COMPLETED
        assert r.generated_text == "This is a test response."


def test_mixed_success_failure(experiment_with_runs, test_db):
    orchestrator = ExperimentOrchestrator(experiment_with_runs, test_db)

    # Side effect: first run fails, second run succeeds
    results = [
        Exception("LLM failure"),  # simulate failure
        {"llm_response": "ok", "metrics": {"score": 1}},  # success
    ]

    def runner_side_effect(*args, **kwargs):
        result = results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    orchestrator.runner.run = MagicMock(side_effect=runner_side_effect)

    result_experiment = orchestrator.run_experiment()

    # The experiment should fail overall because one run failed
    assert result_experiment.status == ExperimentStatus.FAILED

    # Check ResponseRecords
    responses = test_db.query(ResponseRecord).all()
    assert len(responses) == 2
    statuses = [r.status for r in responses]
    assert ResponseStatus.FAILED in statuses
    assert ResponseStatus.COMPLETED in statuses


def test_experiment_status_failed(test_db):
    # Create experiment with 2 runs
    run1 = ExperimentRun(id=1, temperature=0.7, top_p=0.9, max_output_tokens=100)
    run2 = ExperimentRun(id=2, temperature=0.8, top_p=0.85, max_output_tokens=150)
    experiment = Experiment(
        id=1,
        user_prompt="Hello world",
        model_name=DEFAULT_OPENAI_MODEL_NAME,
        runs=[run1, run2],
        status=ExperimentStatus.PENDING,
    )

    orchestrator = ExperimentOrchestrator(experiment, test_db)

    # First run fails, second succeeds
    results = [Exception("LLM failure"), {"llm_response": "ok", "metrics": {}}]

    orchestrator.runner.run = MagicMock(
        side_effect=lambda *a, **kw: (
            results.pop(0)
            if not isinstance(results[0], Exception)
            else (_ for _ in ()).throw(results.pop(0))
        )
    )

    result_experiment = orchestrator.run_experiment()
    assert result_experiment.status == ExperimentStatus.FAILED


def test_skip_already_completed_runs(test_db):
    # Create experiment with 2 runs
    run1 = ExperimentRun(id=1, temperature=0.7, top_p=0.9, max_output_tokens=100)
    run2 = ExperimentRun(id=2, temperature=0.8, top_p=0.85, max_output_tokens=150)
    experiment = Experiment(
        id=1,
        user_prompt="Hello world",
        model_name=DEFAULT_OPENAI_MODEL_NAME,
        runs=[run1, run2],
        status=ExperimentStatus.PENDING,
    )

    # Insert one completed ResponseRecord
    completed_response = ResponseRecord(
        experiment_run=run1,
        status=ResponseStatus.COMPLETED,
        generated_text="done",
        metrics={"score": 1},
    )
    test_db.add(completed_response)
    test_db.commit()

    orchestrator = ExperimentOrchestrator(experiment, test_db)

    # Mock runner to succeed
    orchestrator.runner.run = MagicMock(
        return_value={"llm_response": "new result", "metrics": {"score": 1}}
    )

    result_experiment = orchestrator.run_experiment()

    # Experiment should complete because the second run completed successfully
    assert result_experiment.status == ExperimentStatus.COMPLETED

    # Ensure first run was not called again
    orchestrator.runner.run.assert_called_once()
