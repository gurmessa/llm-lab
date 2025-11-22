import time

from nltk.tokenize import sent_tokenize, word_tokenize
from sqlalchemy.orm import Session

from app.services.core.experiment_runner import ExperimentRunner

from ...db.enums import ExperimentStatus, ResponseStatus
from ...db.models.experiment_models import Experiment, ExperimentRun, ResponseRecord


class ExperimentOrchestrator:
    """
    Orchestrates running all ExperimentRun instances of an Experiment,
    storing responses and metrics, and updating statuses.
    """

    def __init__(self, experiment: Experiment, db_session: Session):
        self.experiment = experiment
        self.db_session = db_session
        self.runner = ExperimentRunner(model_name=experiment.model_name)

    def run_experiment(self):
        """
        Run all pending ExperimentRun instances for the experiment.
        """
        all_success = True

        for run in self.experiment.runs:
            # Check if there's already a ResponseRecord that is not PENDING
            latest_response = (
                self.db_session.query(ResponseRecord)
                .filter(ResponseRecord.experiment_run_id == run.id)
                .order_by(ResponseRecord.created_at.desc())
                .first()
            )

            if latest_response and latest_response.status != ResponseStatus.PENDING:
                continue  # Skip already processed runs

            # Create a new ResponseRecord for this run
            response_record = ResponseRecord(
                experiment_run=run,
                status=ResponseStatus.RUNNING,
            )
            self.db_session.add(response_record)
            self.db_session.commit()

            try:
                start_time = time.time()
                # Run LLM + metrics
                result = self.runner.run(
                    user_prompt=self.experiment.user_prompt,
                    temperature=run.temperature,
                    top_p=run.top_p,
                    max_tokens=run.max_output_tokens,
                )
                end_time = time.time()

                # Fill response record
                generated_text = result.get("llm_response", "")
                metrics = result.get("metrics", {})

                response_record.generated_text = generated_text
                response_record.metrics = metrics
                response_record.latency_ms = (end_time - start_time) * 1000
                response_record.total_words = len(word_tokenize(generated_text))
                response_record.total_sentences = len(sent_tokenize(generated_text))
                response_record.status = ResponseStatus.COMPLETED

            except Exception as e:
                response_record.status = ResponseStatus.FAILED
                response_record.error_message = str(e)

            finally:
                self.db_session.commit()

        # Update experiment status based on all ResponseRecords
        response_statuses = [
            r.status
            for run in self.experiment.runs
            for r in self.db_session.query(ResponseRecord)
            .filter(ResponseRecord.experiment_run_id == run.id)
            .all()
        ]

        if all(s == ResponseStatus.COMPLETED for s in response_statuses):
            self.experiment.status = ExperimentStatus.COMPLETED
        elif any(s == ResponseStatus.RUNNING for s in response_statuses):
            self.experiment.status = ExperimentStatus.RUNNING
        elif any(s == ResponseStatus.FAILED for s in response_statuses):
            self.experiment.status = ExperimentStatus.FAILED

        self.db_session.commit()
        return self.experiment
