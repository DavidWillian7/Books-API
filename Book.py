from typing import Optional
from pydantic import BaseModel, Field

class Book():
    id: int
    title: str
    author: str
    description: str
    rating: float
    published_year: int

    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year

class BookRequest(BaseModel):
    id: Optional[int] = Field(description = "Id is not needed on create.", default = None)
    title: str = Field(min_length = 3)
    author: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length = 200)
    rating: float = Field(ge = 0, le = 10)
    published_year: int = Field(ge = 0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithpython",
                "description": "A new description of a book",
                "rating": 5.7,
                "published_year": 2017
            }
        }
    }