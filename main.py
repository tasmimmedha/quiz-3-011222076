from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

books = {}     # in-memory storage
next_id = 1    # auto-increment ID

class Book(BaseModel):
    title: str
    author: str
    price: float

class BookUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None

# 1. GET all books
@app.get("/books")
def get_all_books():
    return books

# 2. POST /books - Create a book
@app.post("/books", status_code=201)
def create_book(book: Book):
    global next_id
    books[next_id] = book.dict()
    created_book = books[next_id]
    next_id += 1
    return created_book

# 3. PUT /books/{book_id} - Update a book
@app.put("/books/{book_id}")
def update_book(book_id: int, update: BookUpdate):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Not found")
    data = books[book_id]
    if update.title is not None:
        data["title"] = update.title
    if update.price is not None:
        data["price"] = update.price
    return data

# 4. DELETE /books/{book_id} - Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Not found")
    del books[book_id]
    return {"message": "Book deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
