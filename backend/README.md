## Installation Steps

### 1. Create & actviate Virtual Environment
```sh
python3 -m venv myenv
source myenv/bin/activate
```
### 2. Install requirements
```sh
pip install -r requirements.txt
```

### 3. Apply migrations
```sh
alembic upgrade head
```

### 4. Run FastAPI server
```sh
cd backend
uvicorn app.main:app --reload --port=8083
```

### Launch IPython Shell
```sh
python3 -m IPython
```

### Run Tests
```sh
cd backend
pytest -v
```