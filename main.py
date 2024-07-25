from fastapi import FastAPI, status, HTTPException, Path, Query

from Book import Book, BookRequest

app = FastAPI()

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

@app.get("/books", status_code = status.HTTP_200_OK)
async def list_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code = status.HTTP_200_OK)
async def list_book_by_id(book_id: int = Path(ge = 1)):
    for book in BOOKS:
        if book_id == book.id:
            return book
    
    raise HTTPException(status_code = 404, detail="Book not found.")

@app.get("/books/", status_code = status.HTTP_200_OK)
async def list_books_by_rating(book_rating: float = Query(ge = 0, le = 10)):
    books_to_return = []
    for book in BOOKS:
        if book_rating == book.rating:
            books_to_return.append(book)
    
    return books_to_return

@app.get("/books/publish/", status_code = status.HTTP_200_OK)
async def list_books_by_published_year(published_year: int = Query(ge = 0)):
    books_to_return = []
    for book in BOOKS:
        if book.published_year == published_year:
            books_to_return.append(book)
    
    return books_to_return

@app.post("/books", status_code = status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book = set_book_id(new_book)
    BOOKS.append(new_book)
    return new_book

@app.put("/books/{book_id}", status_code = status.HTTP_200_OK)
async def update_book(book_id: int, book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            book.id = book_id
            new_book = Book(**book.model_dump())
            BOOKS[i] = new_book
            return new_book

    raise HTTPException(status_code = 404, detail="Book not found.")

@app.delete("/books/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(ge = 1)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return

    raise HTTPException(status_code = 404, detail="Book not found")

def set_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book