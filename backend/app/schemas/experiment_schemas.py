from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from app.db.enums import ExperimentStatus, ResponseStatus


class ResponseRecordSchema(BaseModel):
    id: int
    generated_text: Optional[str]
    status: ResponseStatus
    error_message: Optional[str]
    latency_ms: Optional[float]
    total_words: Optional[int]
    total_sentences: Optional[int]
    metrics: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class ExperimentRunSchema(BaseModel):
    id: int
    temperature: float
    top_p: float
    max_output_tokens: int
    created_at: datetime
    response: Optional[ResponseRecordSchema] = None

    class Config:
        from_attributes = True


class ExperimentListSchema(BaseModel):
    id: int
    name: Optional[str]
    total_runs: int
    status: ExperimentStatus
    created_at: datetime

    class Config:
        from_attributes = True


class ExperimentDetailSchema(BaseModel):
    id: int
    name: Optional[str]
    total_runs: int
    status: ExperimentStatus
    user_prompt: str
    model_name: str
    created_at: datetime
    updated_at: datetime
    runs: List[ExperimentRunSchema] = []

    class Config:
        from_attributes = True
