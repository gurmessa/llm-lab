import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.enums import ExperimentStatus, ResponseStatus
from app.db.models.experiment_models import Experiment, ExperimentRun, ResponseRecord
from app.db.session import get_db
from app.main import app


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


@pytest.fixture
def client(test_db):
    """Create test client with dependency override"""

    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestExperimentAPI:
    """Test the experiment endpoints"""

    def test_list_experiments_empty(self, client):
        """Test listing experiments when no experiments exist"""
        response = client.get("/experiments/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_experiments(self, client, test_db):
        """Test listing experiments"""
        # Create test experiments
        exp1 = Experiment(
            user_prompt="Test prompt 1",
            name="Experiment 1",
            model_name="gpt-3.5-turbo",
            total_runs=5,
            status=ExperimentStatus.COMPLETED,
        )
        exp2 = Experiment(
            user_prompt="Test prompt 2",
            model_name="gpt-4",
            total_runs=3,
            status=ExperimentStatus.PENDING,
        )

        test_db.add(exp1)
        test_db.add(exp2)
        test_db.commit()
        test_db.refresh(exp1)
        test_db.refresh(exp2)

        response = client.get("/experiments/")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2

        # Check first experiment
        assert data[1]["id"] == exp1.id
        assert data[1]["name"] == "Experiment 1"
        assert data[1]["total_runs"] == 5
        assert data[1]["status"] == "completed"
        assert "created_at" in data[0]

        # Check second experiment
        assert data[0]["id"] == exp2.id
        assert data[0]["name"] is None
        assert data[0]["total_runs"] == 3
        assert data[0]["status"] == "pending"

    def test_get_experiment_detail_not_found(self, client):
        """Test getting experiment detail when experiment doesn't exist"""
        response = client.get("/experiments/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Experiment not found"

    def test_get_experiment_detail_basic(self, client, test_db):
        """Test getting experiment detail without runs"""
        exp = Experiment(
            user_prompt="Test detailed prompt",
            name="Detail Test",
            model_name="gpt-4",
            total_runs=0,
            status=ExperimentStatus.RUNNING,
        )

        test_db.add(exp)
        test_db.commit()
        test_db.refresh(exp)

        response = client.get(f"/experiments/{exp.id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == exp.id
        assert data["name"] == "Detail Test"
        assert data["total_runs"] == 0
        assert data["status"] == "running"
        assert data["user_prompt"] == "Test detailed prompt"
        assert data["model_name"] == "gpt-4"
        assert "created_at" in data
        assert "updated_at" in data
        assert data["runs"] == []

    def test_get_experiment_detail_with_runs_and_responses(self, client, test_db):
        """Test getting experiment detail with runs and responses"""
        # Create experiment
        exp = Experiment(
            user_prompt="Complex test prompt",
            name="Complex Test",
            model_name="gpt-4",
            total_runs=2,
            status=ExperimentStatus.COMPLETED,
        )
        test_db.add(exp)
        test_db.commit()
        test_db.refresh(exp)

        # Create experiment runs
        run1 = ExperimentRun(
            experiment_id=exp.id, temperature=0.7, top_p=0.9, max_output_tokens=1000
        )
        run2 = ExperimentRun(
            experiment_id=exp.id, temperature=0.5, top_p=0.8, max_output_tokens=1500
        )

        test_db.add(run1)
        test_db.add(run2)
        test_db.commit()
        test_db.refresh(run1)
        test_db.refresh(run2)

        # Create responses
        response1 = ResponseRecord(
            experiment_run_id=run1.id,
            generated_text="Test response 1",
            status=ResponseStatus.COMPLETED,
            latency_ms=150.0,
            total_words=10,
            total_sentences=2,
            metrics={"coherence": 0.9, "structure": 0.8},
        )
        response2 = ResponseRecord(
            experiment_run_id=run2.id,
            generated_text="Test response 2",
            status=ResponseStatus.FAILED,
            error_message="API timeout",
            latency_ms=5000.0,
        )

        test_db.add(response1)
        test_db.add(response2)
        test_db.commit()

        response = client.get(f"/experiments/{exp.id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == exp.id
        assert data["name"] == "Complex Test"
        assert len(data["runs"]) == 2

        # Check first run
        run_data_1 = data["runs"][0]
        assert run_data_1["id"] == run1.id
        assert run_data_1["temperature"] == 0.7
        assert run_data_1["top_p"] == 0.9
        assert run_data_1["max_output_tokens"] == 1000
        assert "created_at" in run_data_1

        # Check first response
        resp_data_1 = run_data_1["response"]
        assert resp_data_1["id"] == response1.id
        assert resp_data_1["generated_text"] == "Test response 1"
        assert resp_data_1["status"] == "completed"
        assert resp_data_1["latency_ms"] == 150.0
        assert resp_data_1["total_words"] == 10
        assert resp_data_1["total_sentences"] == 2
        assert resp_data_1["metrics"]["coherence"] == 0.9

        # Check second run
        run_data_2 = data["runs"][1]
        assert run_data_2["id"] == run2.id

        # Check second response
        resp_data_2 = run_data_2["response"]
        assert resp_data_2["status"] == "failed"
        assert resp_data_2["error_message"] == "API timeout"
        assert resp_data_2["generated_text"] == "Test response 2"
