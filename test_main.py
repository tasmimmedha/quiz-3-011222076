import pytest
from fastapi.testclient import TestClient
from main import app, books

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset():
    books.clear()
    import main
    main.next_id = 1
    yield

def test_create_book():
    response = client.post("/books", json={
        "title": "Clean Code", "author": "Robert Martin", "price": 29.99
    })
    assert response.status_code == 201   # must be 201 Created
    # write one more assert below:
    assert response.json()["title"] == "Clean Code"

def test_delete_book():
    # Step 1: create a book first
    client.post("/books", json={
        "title": "Test", "author": "Author", "price": 9.99
    })
    # Step 2: delete the book
    response = client.delete("/books/1")
    assert response.status_code == 200
    # Step 3: verify it is gone
    check = client.get("/books")
    assert len(check.json()) == 0

# Bonus Tests
def test_get_all_books():
    # Create 2 books
    client.post("/books", json={"title": "Book 1", "author": "Author 1", "price": 10.0})
    client.post("/books", json={"title": "Book 2", "author": "Author 2", "price": 20.0})
    # Call GET /books and assert count is 2
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_book():
    # Create a book
    client.post("/books", json={"title": "Original Title", "author": "Author", "price": 15.0})
    # PUT with new price
    response = client.put("/books/1", json={"price": 25.0})
    assert response.status_code == 200
    data = response.json()
    # Assert price changed and title unchanged
    assert data["price"] == 25.0
    assert data["title"] == "Original Title"
