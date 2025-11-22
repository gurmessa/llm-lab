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

### 3. Apply migration
```sh
alembic upgrade head
```

### 4. Run server
```sh
uvicorn main:app --reload --port=8083
```

### Launch IPython
```sh
python3 -m IPython
```

### Run Test
```sh
pytest -v
```