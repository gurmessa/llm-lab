from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

from app.db.enums import ExperimentStatus, ResponseStatus
from app.services.llm.constants import DEFAULT_OPENAI_MODEL_NAME, MAX_OUTPUT_TOKENS


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


class ExperimentRunCreateSchema(BaseModel):
    temperature: float = Field(..., ge=0, le=2)
    top_p: float = Field(..., ge=0, le=1)
    max_output_tokens: int = Field(..., le=MAX_OUTPUT_TOKENS, gt=0)

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


class ExperimentCreateSchema(BaseModel):
    user_prompt: str
    name: Optional[str] = None
    model_name: str = DEFAULT_OPENAI_MODEL_NAME
    total_runs: int
    runs: List[ExperimentRunCreateSchema]

    @validator("name", always=True)
    def set_name_from_prompt(cls, v, values):
        if v is None and "user_prompt" in values:
            return values["user_prompt"][:100]
        return v

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
