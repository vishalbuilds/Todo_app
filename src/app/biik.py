from typing import Optional
from fastapi import FastAPI, Query, Body, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status    
#from row.constant import BOOKS

app=FastAPI()



class Book:
    id: int
    title :str
    author :str
    description: str
    published_date: int
    rating: int

    def __init__(self, id, title, author, description, published_date,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.published_date= published_date
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int]=Field(description="ID is not needed to create a book", default=None)
    title :str= Field(min_length=3)
    author :str
    description: str 
    published_date:int = Field (gt=1900, lt=2025)
    rating: int = Field (lt=6, gt=0)
    model_config ={
        "json_schema_extra": {
            "example":{
                "title": "New Title",
                "author": "New Author",
                "description": "New Description",
                "published_date": 2021,
                "rating": 5
            }
        }
    }


BOOKS =[
    Book(1, "Title One", "Author 1", "Description 1",2021, 5),
    Book(2, "Title Two", "Author 2", "Description 2", 2022,   4), 
    Book(3, "Title Three", "Author 3", "Description 3", 2022, 3),
    Book(4, "Title Four", "Author 4", "Description 4",2021, 5),
    Book(5, "Title Five", "Author 5", "Description 5", 2023, 4)
]


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS

@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book=Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book)) 


def find_book_id(book:Book):
    if len(BOOKS)> 0:
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    return book

@app.get("/books/get_book_by_id/{book_id}",status_code=status.HTTP_200_OK)
async def read_booK_by_id(book_id: int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/search_by_rating/", status_code=status.HTTP_200_OK)
async def read_booK_by_rating(book_rating: int=Query(gt=0, lt=6)):
    books_list=[]
    for book in BOOKS:
        if book.rating==book_rating:
            books_list.append(book)
    return books_list


@app.put("/books/update_book/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_update: BookRequest):
    book_change=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_update.id:
            BOOKS[i]=book_update
            book_change=True
    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books_delete/{book}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book: int=Path(gt=0)):
    book_change=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book:
            BOOKS.pop(i)
            book_change=True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/search_by_date/", status_code=status.HTTP_200_OK)
async def search_by_date(date: int=Query(gt=1900, lt=2025)):
    books_list=[]
    for book in BOOKS:
        if book.published_date==date:
            books_list.append(book)
    return books_list
    