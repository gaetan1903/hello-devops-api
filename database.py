"""Database configuration and models for the DevOps Items API."""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
)  # pylint: disable=import-error
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)  # pylint: disable=import-error

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./devops_items.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


# Database model
class ItemDB(Base):  # pylint: disable=too-few-public-methods
    """Database model for DevOps items."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)


# Create tables
def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    """Get a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
