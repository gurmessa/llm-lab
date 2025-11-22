from fastapi import FastAPI

from app.api.experiment_router import router as experiment_router

app = FastAPI(title="LLM Lab Backend")

app.include_router(experiment_router)
