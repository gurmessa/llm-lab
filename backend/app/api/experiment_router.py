import csv
from io import StringIO
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ..db.models.experiment_models import Experiment, ExperimentRun
from ..db.session import get_db
from ..schemas.experiment_schemas import (
    ExperimentCreateSchema,
    ExperimentDetailSchema,
    ExperimentListSchema,
)
from ..services.core.experiment_orchestrator import ExperimentOrchestrator

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.get("/", response_model=List[ExperimentListSchema])
def list_experiments(db: Session = Depends(get_db)):
    """
    Get list of experiments with basic information
    """
    experiments = db.query(Experiment).order_by(Experiment.created_at.desc()).all()
    return experiments


@router.get("/{experiment_id}", response_model=ExperimentDetailSchema)
def get_experiment_detail(experiment_id: int, db: Session = Depends(get_db)):
    """
    Get detailed experiment information with associated runs and responses
    Returns: experiment details + list of runs with responses
    """
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()

    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return experiment


@router.post("/", response_model=ExperimentDetailSchema)
def create_experiment(
    experiment_data: ExperimentCreateSchema, db: Session = Depends(get_db)
):
    """
    Create a new experiment with associated runs and execute it
    """
    # Create the experiment
    experiment = Experiment(
        user_prompt=experiment_data.user_prompt,
        name=experiment_data.name,
        model_name=experiment_data.model_name,
        total_runs=experiment_data.total_runs,
        status="pending",
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    # Create experiment runs
    for run_data in experiment_data.runs:
        run = ExperimentRun(
            experiment_id=experiment.id,
            temperature=run_data.temperature,
            top_p=run_data.top_p,
            max_output_tokens=run_data.max_output_tokens,
        )
        db.add(run)

    db.commit()

    # Refresh to get all runs
    db.refresh(experiment)

    # Run the experiment orchestrator
    orchestrator = ExperimentOrchestrator(experiment, db)
    experiment = orchestrator.run_experiment()

    return experiment


@router.get("/{experiment_id}/export/csv")
def export_experiment_csv(experiment_id: int, db: Session = Depends(get_db)):
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # Build CSV as string
    csv_file = StringIO()
    writer = csv.writer(csv_file)

    # Header
    writer.writerow(
        ["Run ID", "Temperature", "Top P", "Response Text", "Overall Metric"]
    )

    # Rows
    for run in experiment.runs:
        response = run.response  # because it's one-to-one
        if response:
            writer.writerow(
                [
                    run.id,
                    run.temperature,
                    run.top_p,
                    response.generated_text or "",
                    response.metrics.get("overall") if response.metrics else "",
                ]
            )
    csv_content = csv_file.getvalue()

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=experiment_{experiment_id}.csv"
        },
    )
