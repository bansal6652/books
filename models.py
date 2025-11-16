from typing import List, Optional
from pydantic import BaseModel, Field, computed_field, field_validator , model_validator

class Book(BaseModel):
    # Added the unique integer ID field
    id: Optional[int] = Field(None, description="ID is not needed on create",)
    title : str = Field(... , min_length=3)
    author : str = Field(...)
    tags : List[str] = Field(...)
    price : float = Field(... , gt=0)
    co_author : Optional[str] = None

    @computed_field
    @property
    def discounted_price(self) -> float :
        return round((self.price * 0.8),2)
    
    #if co_author is not provided the author becomes co_author
    @model_validator(mode="after")  
    def default_co_author(self):
        if not self.co_author:
            self.co_author = self.author
        return self
    
    model_config = {
        "json_schema_extra" : {
            "example" : {
                "title" : "A new book",
                "author" : "The author of the book",
                "tags" : ["tag1" , "tag2"],
                "price" : 0.0,
                "co_author" : "This feild is Optional",
            }
        }
    }

class BookPatch(BaseModel):
    # Added the unique integer ID field
    #id: Optional[int] = Field(default=None, description="ID is not needed on create",)
    title : Optional[str] =None
    author : Optional[str] = None
    tags : Optional[List[str]] = None
    price : Optional[float] = None
    co_author : Optional[str] = None

    @field_validator("title")
    def validate_title(cls,v):
        if v is not None and len(v) < 3:
            raise ValueError("Title must have atleast 3 characters")
        return v



BOOKS : List[Book] = [
    Book(
        id=1,
        title="The Serpent's Jewel",
        author="Elias Thorne",
        tags=["Fantasy", "Epic", "Adventure"],
        price=18.50,
        co_author="Lirael Sunstone"
    ),
    Book(
        id=2,
        title="Deep Learning Explained",
        author="Dr. Anya Sharma",
        tags=["Science", "AI", "Technology", "Programming"],
        price=35.99,
        co_author=None
    ),
    Book(
        id=3,
        title="The Midnight Express",
        author="Clara Jennings",
        tags=["Mystery", "Thriller", "Suspense"],
        price=9.99
    ),
    Book(
        id=4,
        title="A History of Quantum Physics",
        author="Professor Isaac Chen",
        tags=["Physics", "Non-Fiction", "Science"],
        price=29.00,
        co_author="Dr. Emily Carter"
    ),
    Book(
        id=5,
        title="Cooking for Beginners",
        author="Chef Ricardo",
        tags=["Cooking", "Food", "Instructional"],
        price=14.25
    )
]

def checkbookid(newbook : Book):
    newbook.id = BOOKS[-1].id+1 if len(BOOKS)>0 else 1
    return newbook