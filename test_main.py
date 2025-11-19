"""Unit tests for the DevOps Items API."""

import pytest  # pylint: disable=import-error
from fastapi.testclient import TestClient  # pylint: disable=import-error
from sqlalchemy import create_engine  # pylint: disable=import-error
from sqlalchemy.orm import sessionmaker  # pylint: disable=import-error

from main import app
from database import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_devops_items.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override get_db dependency
def override_get_db():
    """Override the get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to DevOps Items API"}


def test_get_items_empty():
    """Test getting items when database is empty."""
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item():
    """Test creating a new item."""
    response = client.post("/items", json={"text": "Docker container"})
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Docker container"
    assert "id" in data
    assert data["id"] == 1


def test_create_item_invalid():
    """Test creating an item with invalid data."""
    response = client.post("/items", json={"text": ""})
    assert response.status_code == 422  # Validation error


def test_get_items_with_data():
    """Test getting items after creating some."""
    # Create items
    client.post("/items", json={"text": "Kubernetes"})
    client.post("/items", json={"text": "Jenkins"})

    # Get all items
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["text"] == "Kubernetes"
    assert data[1]["text"] == "Jenkins"


def test_update_item():
    """Test updating an existing item."""
    # Create an item
    create_response = client.post("/items", json={"text": "GitLab"})
    item_id = create_response.json()["id"]

    # Update the item
    update_response = client.put(f"/items/{item_id}", json={"text": "GitLab CI/CD"})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["text"] == "GitLab CI/CD"
    assert data["id"] == item_id


def test_update_item_not_found():
    """Test updating a non-existent item."""
    response = client.put("/items/999", json={"text": "Updated"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_delete_item():
    """Test deleting an item."""
    # Create an item
    create_response = client.post("/items", json={"text": "Ansible"})
    item_id = create_response.json()["id"]

    # Delete the item
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204

    # Verify it's deleted
    get_response = client.get("/items")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0


def test_delete_item_not_found():
    """Test deleting a non-existent item."""
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_crud_workflow():
    """Test complete CRUD workflow."""
    # Create
    create_response = client.post("/items", json={"text": "Terraform"})
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    # Read
    get_response = client.get("/items")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1

    # Update
    update_response = client.put(f"/items/{item_id}", json={"text": "Terraform Cloud"})
    assert update_response.status_code == 200
    assert update_response.json()["text"] == "Terraform Cloud"

    # Delete
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204

    # Verify empty
    final_get_response = client.get("/items")
    assert final_get_response.status_code == 200
    assert len(final_get_response.json()) == 0
