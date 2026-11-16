import src.book as Book
import src.slideshow as Slideshow
from src.display import MockDisplay

COVERS = [
    "books/media/ideogram_1.jpeg",
    "books/media/ideogram_2.jpeg",
    "books/media/ideogram_3.jpeg",
]


def make_books():
    return [Book.Book(f"title{i}", "author", cover, "2024-01-01") for i, cover in enumerate(COVERS)]


def test_run_shows_next_book_and_wraps_around():
    display = MockDisplay()
    show = Slideshow.slideshow(600, make_books(), display)

    for cover in COVERS + [COVERS[0]]:
        show.run()
        assert display.last_image_path == cover


def test_run_wakes_display():
    display = MockDisplay()
    show = Slideshow.slideshow(600, make_books(), display)

    show.run()

    assert display.woke is True


def test_interrupt_update_fires_after_interval(monkeypatch):
    display = MockDisplay()
    show = Slideshow.slideshow(600, make_books(), display)
    assert show.interrupt_update is False

    future = Slideshow.time.time() + Slideshow.UPDATE_INTERVAL + 1
    monkeypatch.setattr(Slideshow.time, "time", lambda: future)
    show.run()

    assert show.interrupt_update is True


def test_run_with_empty_book_list_does_not_crash():
    display = MockDisplay()
    show = Slideshow.slideshow(600, [], display)

    show.run()

    assert display.last_image_path is None


def test_update_done_resets_state():
    display = MockDisplay()
    show = Slideshow.slideshow(600, make_books(), display)
    show.interrupt_update = True

    show.update_done(make_books())

    assert show.interrupt_update is False
