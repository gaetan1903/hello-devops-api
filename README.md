# hello-devops-api

A FastAPI-based REST API for managing DevOps items with SQLite database.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Pydantic models for request/response validation
- ✅ CORS configured for React frontend (localhost:5173)
- ✅ Comprehensive unit tests with pytest
- ✅ Auto-generated API documentation (Swagger UI)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root
- `GET /` - Welcome message

### Items
- `GET /items` - Get all items
- `POST /items` - Create a new item
  - Body: `{"text": "string"}`
  - Returns: `{"id": int, "text": "string"}`
- `PUT /items/{id}` - Update an item
  - Body: `{"text": "string"}`
  - Returns: `{"id": int, "text": "string"}`
- `DELETE /items/{id}` - Delete an item
  - Returns: 204 No Content

## API Documentation

Once the server is running, access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

Run all tests:
```bash
pytest test_main.py -v
```

Run with coverage:
```bash
pytest test_main.py -v --cov=.
```

## Project Structure

```
.
├── main.py           # FastAPI application and endpoints
├── models.py         # Pydantic models for validation
├── database.py       # SQLAlchemy database configuration
├── test_main.py      # Unit tests
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```

## Database

The API uses SQLite database (`devops_items.db`) which is created automatically on first run.

## CORS Configuration

CORS is configured to allow requests from:
- `http://localhost:5173` (React development server)

To add more origins, modify the `allow_origins` list in `main.py`.

## Example Usage

### Create an item
```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"text": "Docker"}'
```

### Get all items
```bash
curl http://localhost:8000/items
```

### Update an item
```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"text": "Docker & Kubernetes"}'
```

### Delete an item
```bash
curl -X DELETE http://localhost:8000/items/1
```