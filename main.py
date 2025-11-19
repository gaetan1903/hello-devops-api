from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager

from database import get_db, init_db, ItemDB
from models import Item, ItemCreate, ItemUpdate


# Initialize database on startup using lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (if needed)


# Initialize FastAPI app
app = FastAPI(
    title="DevOps Items API",
    description="API for managing DevOps items",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to DevOps Items API"}


# GET /items - Retrieve all items
@app.get("/items", response_model=List[Item])
def get_items(db: Session = Depends(get_db)):
    items = db.query(ItemDB).all()
    return items


# POST /items - Create a new item
@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemDB(text=item.text)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# PUT /items/{id} - Update an item
@app.put("/items/{id}", response_model=Item)
def update_item(id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.text = item.text
    db.commit()
    db.refresh(db_item)
    return db_item


# DELETE /items/{id} - Delete an item
@app.delete("/items/{id}", status_code=204)
def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return None
