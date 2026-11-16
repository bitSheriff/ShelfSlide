# import the test framework
import pytest
from unittest.mock import MagicMock

# import the code to be tested
import sys
sys.path.append("..")
import shelfslide
import src.book as Book

def test_load_simple_bookLibrary():

    list = shelfslide.load_simple_bookLibrary(".")

    # list must be empty
    assert len(list) == 0

    pass


def test_generate_coverfilename():
    assert shelfslide.generate_coverfilename("J.R.R. Tolkien", "The Hobbit") == "j.r.r.-tolkien_the-hobbit.jpg"


def test_file_is_media_accepts_known_extensions():
    assert shelfslide.file_is_media("doc/logo.jpeg")
    assert shelfslide.file_is_media("books/media/ideogram_1.jpeg")


def test_file_is_media_rejects_unknown_extension():
    assert not shelfslide.file_is_media("README.md")


def test_file_is_media_rejects_missing_file():
    assert not shelfslide.file_is_media("books/media/does-not-exist.jpg")


def test_sort_books_asc_orders_by_date():
    books = [
        Book.Book("B", "x", "c", "2024-03-01"),
        Book.Book("A", "x", "c", "2024-01-01"),
    ]
    result = shelfslide.sort_books(books, "asc")
    assert [b.title for b in result] == ["A", "B"]


def test_sort_books_desc_orders_by_date():
    books = [
        Book.Book("A", "x", "c", "2024-01-01"),
        Book.Book("B", "x", "c", "2024-03-01"),
    ]
    result = shelfslide.sort_books(books, "desc")
    assert [b.title for b in result] == ["B", "A"]


def test_sort_books_unknown_mode_returns_unchanged():
    books = [Book.Book("A", "x", "c", "1"), Book.Book("B", "x", "c", "2")]
    assert shelfslide.sort_books(books, "unknown") == books