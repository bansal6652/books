from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
from typing import List,Dict, Optional
#from prometheus_fastapi_instrumentator import Instrumentator
from models import Book, BOOKS, checkbookid, BookPatch

app = FastAPI(title="BOOKS API")

# Add metrics
# Add metrics BEFORE the app starts (correct way)
#Instrumentator().instrument(app).expose(app)




@app.get("/")
async def landing_page():
    return {"message" : " THis is the Landing Page"}

@app.get("/books/")
async def list_all_books(id:Optional[int] = None, title : Optional[str] = None,
                         author : Optional[str] = None,
                         tag : Optional[str] =None):
    if id is None and title is None and author is None and tag is None:
        return BOOKS
    
    result : List[Book] = []
    if id:
        result = [
            book for book in BOOKS if book.id == id
        ]

    elif title :
        result = [
            book for book in BOOKS if book.title.casefold() == title.casefold()
        ]
    elif author :
        result = [
            book for book in BOOKS if book.author.casefold() == author.casefold()
        ]
    elif tag:
        for book in BOOKS:
            for i in book.tags:
                if tag.casefold() == i.casefold():
                    result.append(book)

    return result



@app.post("/books/addbook")
async def add_new_book(book : Book):
    BOOKS.append(checkbookid(book))    
    return book


@app.put("/book/updatebook")
async def update_book_detail(updatedbook : Book):
    for index,book in enumerate(BOOKS):
        if updatedbook.id == book.id:
            BOOKS[index]= updatedbook
            return BOOKS[index]
        
    return {"MESSAGE " : f"No Book with {updatedbook.id} was found."}

@app.patch("/book/updatebook/{book_id}")
async def update_specific_book_detail(book_id : int , patchbook : BookPatch):
    print(patchbook)
    for book in BOOKS:
        if book.id == book_id:
            if patchbook.title is not None:
                book.title = patchbook.title
            if patchbook.author is not None:
                book.author = patchbook.author
                if patchbook.co_author is None:
                    book.co_author = patchbook.author
            if patchbook.tags is not None:
                book.tags = patchbook.tags
            if patchbook.price is not None:
                book.price = patchbook.price
            if patchbook.co_author is not None:
                book.co_author = patchbook.co_author
            return book
    raise HTTPException(
        status_code=404,
        detail=f"No book with if {book_id} was found"
    )

@app.delete("/book/deletebook/{bookid}")
async def delete_a_book(bookid : int):
    for index,book in enumerate(BOOKS):
        if book.id == bookid:
            dropped_book = BOOKS.pop(index) 
            return dropped_book
    raise HTTPException(
        status_code=404,
        detail=f"No user with id as {bookid} was found"
    )

    





