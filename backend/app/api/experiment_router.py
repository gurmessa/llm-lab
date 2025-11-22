from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db.models.experiment_models import Experiment
from ..db.session import get_db
from ..schemas.experiment_schemas import ExperimentDetailSchema, ExperimentListSchema

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
