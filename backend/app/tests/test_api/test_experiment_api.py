from unittest.mock import MagicMock, patch

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
from app.services.llm.constants import DEFAULT_OPENAI_MODEL_NAME


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
        response = client.get("/experiments/999/")
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

        response = client.get(f"/experiments/{exp.id}/")
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

        response = client.get(f"/experiments/{exp.id}/")
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


class TestCreateExperimentAPI:
    @patch("app.api.experiment_router.ExperimentOrchestrator")
    def test_create_experiment_success(self, mock_orchestrator, client, test_db):
        """Test creating a new experiment successfully with mocked orchestrator"""
        # Setup mock
        mock_experiment = MagicMock()
        mock_experiment.id = 1
        mock_experiment.user_prompt = "Test experiment prompt for validation"
        mock_experiment.name = "Test experiment prompt for validation"
        mock_experiment.model_name = DEFAULT_OPENAI_MODEL_NAME
        mock_experiment.total_runs = 2
        mock_experiment.status = "pending"
        mock_experiment.runs = []

        mock_orchestrator_instance = mock_orchestrator.return_value
        mock_orchestrator_instance.run_experiment.return_value = mock_experiment

        experiment_data = {
            "user_prompt": "Test experiment prompt for validation",
            "total_runs": 2,
            "runs": [
                {"temperature": 0.7, "top_p": 0.9, "max_output_tokens": 1000},
                {"temperature": 1.0, "top_p": 0.8, "max_output_tokens": 500},
            ],
        }

        response = client.post("/experiments/", json=experiment_data)
        assert response.status_code == 200

        data = response.json()
        assert data["user_prompt"] == "Test experiment prompt for validation"
        assert (
            data["name"] == "Test experiment prompt for validation"
        )  # Auto-generated from prompt
        assert data["model_name"] == DEFAULT_OPENAI_MODEL_NAME
        assert data["total_runs"] == 2

        # Verify that the orchestrator was called
        mock_orchestrator.assert_called_once()
        mock_orchestrator_instance.run_experiment.assert_called_once()

    @patch("app.api.experiment_router.ExperimentOrchestrator")
    def test_create_experiment_with_custom_name_and_model(
        self, mock_orchestrator, client, test_db
    ):
        """Test creating experiment with custom name and model with mocked orchestrator"""
        # Setup mock
        mock_experiment = MagicMock()
        mock_experiment.id = 1
        mock_experiment.user_prompt = "Test with custom name"
        mock_experiment.name = "Custom Experiment Name"
        mock_experiment.model_name = "gpt-4.1-mini"
        mock_experiment.total_runs = 1
        mock_experiment.status = "pending"
        mock_experiment.runs = []

        mock_orchestrator_instance = mock_orchestrator.return_value
        mock_orchestrator_instance.run_experiment.return_value = mock_experiment

        experiment_data = {
            "user_prompt": "Test with custom name",
            "name": "Custom Experiment Name",
            "model_name": "gpt-4.1-mini",
            "total_runs": 1,
            "runs": [{"temperature": 0.5, "top_p": 0.95, "max_output_tokens": 1500}],
        }

        response = client.post("/experiments/", json=experiment_data)
        assert response.status_code == 200

        data = response.json()
        assert data["user_prompt"] == "Test with custom name"
        assert data["name"] == "Custom Experiment Name"
        assert data["model_name"] == "gpt-4.1-mini"
        assert data["total_runs"] == 1

        # Verify that the orchestrator was called
        mock_orchestrator.assert_called_once()
        mock_orchestrator_instance.run_experiment.assert_called_once()

    def test_create_experiment_auto_generate_name(self, client, test_db):
        """Test that name is auto-generated from first 100 characters of prompt"""
        long_prompt = "This is a very long prompt that exceeds one hundred characters to test the auto-generation of experiment names from the first 100 characters of the user prompt."
        expected_name = long_prompt[:100]

        experiment_data = {
            "user_prompt": long_prompt,
            "total_runs": 1,
            "runs": [{"temperature": 0.7, "top_p": 0.9, "max_output_tokens": 1000}],
        }

        # Mock the orchestrator to avoid actual execution
        with patch(
            "app.api.experiment_router.ExperimentOrchestrator"
        ) as mock_orchestrator:
            mock_experiment = MagicMock()
            mock_experiment.id = 1
            mock_experiment.user_prompt = long_prompt
            mock_experiment.name = expected_name
            mock_experiment.model_name = DEFAULT_OPENAI_MODEL_NAME
            mock_experiment.total_runs = 1
            mock_experiment.status = "pending"
            mock_experiment.runs = []

            mock_orchestrator_instance = mock_orchestrator.return_value
            mock_orchestrator_instance.run_experiment.return_value = mock_experiment

            response = client.post("/experiments/", json=experiment_data)
            assert response.status_code == 200

            data = response.json()
            assert data["name"] == expected_name

    def test_create_experiment_validation_errors(self, client, test_db):
        """Test validation errors for experiment creation"""
        # Test temperature out of range
        experiment_data = {
            "user_prompt": "Test validation errors",
            "total_runs": 1,
            "runs": [
                {
                    "temperature": 3.0,  # Invalid: should be 0-2
                    "top_p": 0.9,
                    "max_output_tokens": 1000,
                }
            ],
        }

        response = client.post("/experiments/", json=experiment_data)
        assert response.status_code == 422

        # Test top_p out of range
        experiment_data["runs"][0]["temperature"] = 1.0
        experiment_data["runs"][0]["top_p"] = 1.5  # Invalid: should be 0-1

        response = client.post("/experiments/", json=experiment_data)
        assert response.status_code == 422

        # Test max_output_tokens out of range
        experiment_data["runs"][0]["top_p"] = 0.9
        experiment_data["runs"][0][
            "max_output_tokens"
        ] = 2500  # Invalid: should be <= 2000

        response = client.post("/experiments/", json=experiment_data)
        assert response.status_code == 422

    @patch("app.api.experiment_router.ExperimentOrchestrator")
    def test_create_experiment_db_and_orchestrator(
        self, mock_orchestrator, client, test_db
    ):
        """
        Test experiment creation in DB while mocking only the orchestrator execution
        """
        # Setup mock orchestrator to return the experiment as is
        mock_orchestrator_instance = mock_orchestrator.return_value
        mock_orchestrator_instance.run_experiment.side_effect = lambda: test_db.query(
            Experiment
        ).first()

        experiment_data = {
            "user_prompt": "Test experiment prompt",
            "total_runs": 2,
            "runs": [
                {"temperature": 0.7, "top_p": 0.9, "max_output_tokens": 1000},
                {"temperature": 1.0, "top_p": 0.8, "max_output_tokens": 500},
            ],
        }

        # Call the API
        response = client.post("/experiments/", json=experiment_data)
        assert response.status_code == 200

        # Verify DB entries
        exp_in_db = test_db.query(Experiment).first()
        assert exp_in_db is not None
        assert exp_in_db.user_prompt == "Test experiment prompt"
        assert exp_in_db.total_runs == 2

        runs_in_db = (
            test_db.query(ExperimentRun).filter_by(experiment_id=exp_in_db.id).all()
        )
        assert len(runs_in_db) == 2
        assert runs_in_db[0].temperature == 0.7
        assert runs_in_db[1].max_output_tokens == 500

        # Verify orchestrator was called
        mock_orchestrator.assert_called_once()
        mock_orchestrator_instance.run_experiment.assert_called_once()


class TestExportExperimentCSVAPI:
    def test_export_experiment_csv(self, client, test_db):
        # Create experiment
        experiment = Experiment(
            name="Test Experiment",
            user_prompt="Test prompt",
            model_name=DEFAULT_OPENAI_MODEL_NAME,
            total_runs=1,
            status=ExperimentStatus.COMPLETED.value,
        )
        test_db.add(experiment)
        test_db.commit()

        # Create run
        run = ExperimentRun(
            experiment_id=experiment.id,
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=1000,
        )

        test_db.add(run)
        test_db.commit()

        # Create response with metric
        response = ResponseRecord(
            experiment_run_id=run.id,
            generated_text="Test response",
            status=ResponseStatus.COMPLETED.value,
            metrics={"overall_score": 0.95},
        )
        test_db.add(response)
        test_db.commit()

        # Call the CSV export endpoint
        resp = client.get(f"/experiments/{experiment.id}/export/csv/")

        assert resp.status_code == 200
        assert "text/csv" in resp.headers["content-type"]
        assert (
            f"attachment; filename=experiment_{experiment.id}.csv"
            in resp.headers["content-disposition"]
        )

        csv_content = resp.content.decode()
        assert "Run ID,Temperature,Top P,Response Text,Overall Metric" in csv_content
        assert "1,0.7,0.9,Test response," in csv_content  # metric is None, so empty
