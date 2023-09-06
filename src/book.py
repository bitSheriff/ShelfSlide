##
# @brief Book class
# @note This class is used to store the book information
class Book:
    title: str
    author: str
    cover: str
    date: str

    ##
    # @brief Book class constructor
    def __init__(self, title, author, cover,date) -> None:
        self.title = title
        self.author = author
        self.cover = cover
        self.date = date

    ##
    # @brief Book class string representation
    def __str__(self) -> str:
        return f"{self.title} by {self.author} ({self.date}) : {self.cover}\n"
    
    ##
    # @brief Set the cover of the book
    def set_cover(self, cover) -> None:
        self.cover = cover

    def get_cover(self) -> str:
        return self.cover

    ##
    # @brief Set the title of the book
    def set_title(self, title) -> None:
        self.title = title

    ##
    # @brief Set the author of the book
    def set_author(self, author) -> None:
        self.author = author

    ##
    # @brief Set the date of the book
    def set_date(self, date) -> None:
        self.date = date