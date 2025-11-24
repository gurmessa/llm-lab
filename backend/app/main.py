from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.experiment_router import router as experiment_router

app = FastAPI(title="LLM Lab Backend")

app.router.redirect_slashes = False

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # <-- Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # <-- Allows all headers
)


app.include_router(experiment_router)
