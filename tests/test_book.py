import src.book as Book


def test_str_repr():
    b = Book.Book("Title", "Author", "cover.jpg", "2024-01-01")
    assert str(b) == "Title by Author (2024-01-01) : cover.jpg\n"


def test_setters_update_state():
    b = Book.Book("t", "a", "c", "d")

    b.set_title("new title")
    b.set_author("new author")
    b.set_date("2025-01-01")
    b.set_cover("new_cover.jpg")

    assert b.title == "new title"
    assert b.author == "new author"
    assert b.date == "2025-01-01"
    assert b.get_cover() == "new_cover.jpg"
