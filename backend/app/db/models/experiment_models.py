import uuid

from sqlalchemy import JSON, Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..base import Base, TimestampMixin
from ..enums import ExperimentStatus, ResponseStatus


class Experiment(TimestampMixin, Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_prompt = Column(Text, nullable=False)
    name = Column(String(255), nullable=True)
    model_name = Column(String(100), nullable=False)
    total_runs = Column(Integer, default=0)
    status = Column(SQLEnum(ExperimentStatus), default=ExperimentStatus.PENDING)

    # Relationships
    runs = relationship("ExperimentRun", back_populates="experiment")


class ExperimentRun(TimestampMixin, Base):
    __tablename__ = "experiment_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    temperature = Column(Float, nullable=False)
    top_p = Column(Float, nullable=False)
    max_output_tokens = Column(Integer, nullable=False)

    # Relationships
    experiment = relationship("Experiment", back_populates="runs")
    response = relationship(
        "ResponseRecord", back_populates="experiment_run", uselist=False
    )


class ResponseRecord(TimestampMixin, Base):
    __tablename__ = "response_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    experiment_run_id = Column(
        Integer, ForeignKey("experiment_runs.id"), nullable=False
    )
    generated_text = Column(Text, nullable=True)
    status = Column(SQLEnum(ResponseStatus), default=ResponseStatus.PENDING)
    error_message = Column(Text, nullable=True)
    latency_ms = Column(Float, nullable=True)
    total_words = Column(Integer, nullable=True)
    total_sentences = Column(Integer, nullable=True)
    metrics = Column(
        JSON, nullable=True
    )  # e.g., {"coherence": 0.9, "structure": 0.8, "overall": 0.85}

    # Relationships
    experiment_run = relationship("ExperimentRun", back_populates="response")
