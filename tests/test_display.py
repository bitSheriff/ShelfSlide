import pytest

from src.display import Display, MockDisplay, create_display

LOGO = "doc/logo.jpeg"


def test_mock_display_is_a_display():
    assert isinstance(MockDisplay(), Display)


def test_display_image_resizes_to_configured_canvas():
    d = MockDisplay(width=400, height=300)
    d.display_image(LOGO)
    assert d._image.size == (400, 300)


def test_display_image_tracks_last_path():
    d = MockDisplay()
    d.display_image(LOGO)
    assert d.last_image_path == LOGO


def test_display_logo_uses_logo_path():
    d = MockDisplay()
    d.display_logo()
    assert d.last_image_path == LOGO


def test_wake_and_clear_are_tracked():
    d = MockDisplay()
    assert d.woke is False
    assert d.cleared is False

    d.display_wakeUp()
    d.display_clear()

    assert d.woke is True
    assert d.cleared is True


def test_create_display_mock_driver_returns_mock_display():
    d = create_display("epd7in5_V2", 800, 480, "BW", False, driver="mock")
    assert isinstance(d, MockDisplay)


def test_create_display_rejects_unknown_epd_before_touching_hardware():
    # type check happens before any hardware import, so this must not
    # require epaper/RPi.GPIO to be installed
    with pytest.raises(NotImplementedError):
        create_display("some_unknown_epd", 800, 480, "BW", False, driver="waveshare")
