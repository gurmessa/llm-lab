import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ...db.base import Base
from ...db.enums import ExperimentStatus, ResponseStatus
from ...db.models.experiment_models import Experiment, ExperimentRun, ResponseRecord


@pytest.fixture(scope="function")
def test_db():
    """Create an in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()


class TestModels:
    """Minimal tests for models with DB save and relationships"""

    def test_experiment_creation_and_defaults(self, test_db):
        experiment = Experiment(
            user_prompt="Test prompt",
            model_name="gpt-3.5-turbo",
        )
        test_db.add(experiment)
        test_db.commit()
        test_db.refresh(experiment)

        # Check fields
        assert experiment.user_prompt == "Test prompt"
        assert experiment.model_name == "gpt-3.5-turbo"
        assert experiment.name is None
        # Match your model defaults
        assert experiment.total_runs == 0
        assert experiment.status == ExperimentStatus.PENDING
        assert experiment.created_at is not None
        assert experiment.updated_at is not None

    def test_experiment_run_creation_and_relationship(self, test_db):
        experiment = Experiment(user_prompt="Prompt", model_name="gpt-3.5-turbo")
        test_db.add(experiment)
        test_db.commit()
        test_db.refresh(experiment)

        run = ExperimentRun(
            experiment_id=experiment.id,
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=1000,
        )
        test_db.add(run)
        test_db.commit()
        test_db.refresh(run)

        # Check fields
        assert run.experiment_id == experiment.id
        assert run.temperature == 0.7
        assert run.top_p == 0.9
        assert run.max_output_tokens == 1000

        # Check relationship
        assert run.experiment == experiment
        assert run in experiment.runs

    def test_response_record_creation_and_relationship(self, test_db):
        experiment = Experiment(user_prompt="Prompt", model_name="gpt-3.5-turbo")
        test_db.add(experiment)
        test_db.commit()
        test_db.refresh(experiment)

        run = ExperimentRun(
            experiment_id=experiment.id,
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=1000,
        )
        test_db.add(run)
        test_db.commit()
        test_db.refresh(run)

        response = ResponseRecord(
            experiment_run_id=run.id,
            generated_text="Test response",
            status=ResponseStatus.COMPLETED,
            latency_ms=150.0,
            total_words=10,
            total_sentences=2,
            metrics={"coherence": 0.9, "structure": 0.8, "overall": 0.85},
        )
        test_db.add(response)
        test_db.commit()
        test_db.refresh(response)

        # Check fields
        assert response.experiment_run_id == run.id
        assert response.generated_text == "Test response"
        assert response.status == ResponseStatus.COMPLETED
        assert response.latency_ms == 150.0
        assert response.total_words == 10
        assert response.total_sentences == 2
        assert response.metrics == {"coherence": 0.9, "structure": 0.8, "overall": 0.85}

        # Check relationship
        assert response.experiment_run == run
        assert run.response == response
