
class Book:
    title: str
    author: str
    cover: str
    date: str

    def __init__(self, title, author, cover,date) -> None:
        self.title = title
        self.author = author
        self.cover = cover
        self.date = date

    def __str__(self) -> str:
        return f"Book: {self.title} by {self.author} ({self.date})"
    
    def set_cover(self, cover):
        self.cover = cover