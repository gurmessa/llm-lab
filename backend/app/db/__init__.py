import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# -----------------------
# Enums
# -----------------------
class ExperimentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class ResponseStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


# -----------------------
# Models
# -----------------------
class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_prompt = Column(Text, nullable=False)
    name = Column(String(255), nullable=True)
    model_name = Column(String(100), nullable=False)
    total_runs = Column(Integer, default=0)
    status = Column(SQLEnum(ExperimentStatus), default=ExperimentStatus.PENDING)

    # Relationships
    runs = relationship("ExperimentRun", back_populates="experiment")


class ExperimentRun(Base):
    __tablename__ = "experiment_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_id = Column(
        UUID(as_uuid=True), ForeignKey("experiments.id"), nullable=False
    )
    temperature = Column(Float, nullable=False)
    top_p = Column(Float, nullable=False)
    max_output_tokens = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    experiment = relationship("Experiment", back_populates="runs")
    response = relationship(
        "ResponseRecord", back_populates="experiment_run", uselist=False
    )


class ResponseRecord(Base):
    __tablename__ = "response_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_run_id = Column(
        UUID(as_uuid=True), ForeignKey("experiment_runs.id"), nullable=False
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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    experiment_run = relationship("ExperimentRun", back_populates="response")
