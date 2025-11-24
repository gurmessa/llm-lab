# LLM Lab Backend

LLM Lab is a platform for running controlled experiments with Large Language Models (LLMs). This backend service provides the API, data management, and experiment orchestration capabilities.

## Table of Contents
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Quick Start Guide](#quick-start-guide)
- [API Documentation](#api-documentation)
- [Development](#development)

## Tech Stack

- **Language**: Python 3.11
- **Framework**: FastAPI - Modern, fast web framework for building APIs
- **Database**: SQLite with SQLAlchemy ORM
- **Database Migrations**: Alembic
- **Schema**: Pydantic
- **ORM**: SQLAlchemy
- **Embedding**: OpenAI Embedding
- **LLM Integration**: OpenAI API
- **Text Processing**: NLTK
- **Containerization**: Docker
- **Testing**: Pytest
- **Code Quality**: Black (formatter), Isort (import sorter)

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│   Frontend      │───▶│   FastAPI        │───▶│   SQLite Database  │
│   (Next.js)     │    │   Backend        │    │   (via SQLAlchemy) │
└─────────────────┘    └──────────────────┘    └────────────────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │   OpenAI API       │
                     │   Integration      │
                     └────────────────────┘
                                │
                                ▼
                   ┌──────────────────────────┐
                   │   Metrics Calculation    │
                   │   (Coherence, Relevance, │
                   │    Structure, Diversity) │
                   └──────────────────────────┘
```

### Core Components

1. **API Layer** (`app/api/`)
   - FastAPI routers handling HTTP requests
   - Request/response validation using Pydantic schemas

2. **Service Layer** (`app/services/`)
   - Business logic implementation
   - Experiment orchestration
   - LLM integration (OpenAI)
   - Metrics calculation (multiple types)

3. **Data Layer** (`app/db/`)
   - SQLAlchemy models for database entities
   - Database session management
   - Enum definitions

4. **Schema Layer** (`app/schemas/`)
   - Pydantic models for request/response validation

## Project Structure

```
backend/
├── app/                    # Main application code
│   ├── api/               # API routers and endpoints
│   ├── db/                # Database models and session
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   │   ├── core/          # Experiment orchestration
│   │   ├── embedding/     # Embedding services
│   │   ├── llm/           # LLM integration
│   │   └── metrics/       # Evaluation metrics
│   └── tests/             # Test suite
├── alembic/               # Database migrations
├── data/                  # Data storage directory
├── nginx/                 # Nginx configuration
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Multi-container setup
├── requirements.txt       # Python dependencies
└── alembic.ini            # Alembic configuration
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- OpenAI API key

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd llm-lab/backend
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Download NLTK data**
   ```bash
   python -m nltk.downloader punkt punkt_tab
   ```

6. **Initialize the database**
   ```bash
   alembic upgrade head
   ```
7. Run FastAPI server
   ```sh
   cd backend
   uvicorn app.main:app --reload --port=8083
   ```

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Apply database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

## Quick Start Guide

### Running the Application Locally

```bash
# Activate virtual environment
source myenv/bin/activate

# Start the FastAPI server
uvicorn app.main:app --reload --port=8083
```

The API will be available at `http://localhost:8083`

### Running Tests

```bash
# Run all tests
pytest -v

# Run specific test suite
pytest app/tests/test_metrics/ -v
```

### API Usage Example

1. **Create an experiment**
   ```bash
   curl -X POST "http://localhost:8083/experiments/" \
        -H "Content-Type: application/json" \
        -d '{
          "user_prompt": "Write a short story about a robot learning to paint",
          "name": "Robot Artist Experiment",
          "model_name": "gpt-4.1-nano",
          "total_runs": 2,
          "runs": [
            {"temperature": 0.5, "top_p": 1.0, "max_output_tokens": 150},
            {"temperature": 0.8, "top_p": 1.0, "max_output_tokens": 150}
          ]
        }'
   ```

2. **Get experiment results**
   ```bash
   curl "http://localhost:8083/experiments/1/"
   ```

3. **Get previous experiments list**
   ```bash
   curl "http://localhost:8083/experiments/"
   ```

4. **Export results as CSV**
   ```bash
   curl "http://localhost:8083/experiments/1/export/csv/" -o experiment_1.csv
   ```

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: `http://localhost:8083/docs`
- **ReDoc**: `http://localhost:8083/redoc`

### Main Endpoints

- `GET /experiments/` - List all experiments
- `POST /experiments/` - Create a new experiment
- `GET /experiments/{experiment_id}/` - Get detailed experiment information
- `GET /experiments/{experiment_id}/export/csv/` - Export experiment results as CSV

## Development

### Adding New Metrics

1. Create a new metric class in `app/services/metrics/`
2. Inherit from the `Metric` base class
3. Implement the `compute` method
4. Register the metric in `OverallMetric` class

### Adding New LLM Providers

1. Create a new responder class in `app/services/llm/`
2. Implement the `run` method
3. Add the provider to the experiment runner

### Adding New embedding 
1. Create a new embedding class in `app/services/embedding/`
2. Implement the `embed` method


### Database Migrations

When making changes to database models:

1. **Generate a new migration**
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. **Apply migrations**
   ```bash
   alembic upgrade head
   ```

### Code Quality

- Format code with Black: `black .`
- Sort imports with Isort: `isort .`
- Run tests: `pytest`

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)

## Directory Data Persistence

The `data/` directory contains the SQLite database file (`llm_lab.db`) and is mounted as a volume in Docker to persist data between container restarts.
