import logging
import platform
from abc import ABC, abstractmethod

from PIL import Image

KNOWN_EPDs = ["epd7in5_V2"]


##
# @brief Display abstraction
# @note Owns image preparation (resize/rotate/color conversion), which is
# hardware-independent. Subclasses only implement the actual I/O primitives.
class Display(ABC):

    def __init__(self, width, height, colors, rot_inv) -> None:
        self._width = width
        self._height = height
        self._colors = colors
        self._rot = -90 if rot_inv else 90
        self._image = None

    def display_image(self, path) -> None:
        image = self._load_image(path)
        self._image = self._resize_image(image)
        self._send(self._image)

    def display_logo(self) -> None:
        self.display_image("doc/logo.jpeg")

    def display_clear(self) -> None:
        self._clear()

    def display_wakeUp(self) -> None:
        self._wake()

    def _load_image(self, path):
        image = Image.open(path)
        if self._colors == "BW":
            image = image.convert(mode="L")
        return image

    def _resize_image(self, image):
        image = image.rotate(self._rot, expand=True)
        canvas = Image.new("RGB", (self._width, self._height), "white")

        pic_scale = max((image.width / self._width), (image.height / self._height))
        image = image.resize((int(image.width // pic_scale), int(image.height // pic_scale)))

        x_offset = (self._width - image.width) // 2
        y_offset = (self._height - image.height) // 2
        canvas.paste(image, (x_offset, y_offset))
        return canvas

    ##
    # @brief Send a prepared image to the physical/virtual device
    @abstractmethod
    def _send(self, image) -> None: ...

    @abstractmethod
    def _clear(self) -> None: ...

    @abstractmethod
    def _wake(self) -> None: ...


##
# @brief Waveshare e-paper driver (real hardware)
class WaveshareDisplay(Display):

    def __init__(self, type, width, height, colors, rot_inv) -> None:
        super().__init__(width, height, colors, rot_inv)

        if type not in KNOWN_EPDs:
            raise NotImplementedError(f"unsupported EPD: {type}")

        self._type = type
        self._epd = None
        self._init_epd()

    def _init_epd(self) -> None:
        import epaper
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BCM)
        self._epd = epaper.epaper(self._type).EPD()
        self._epd.init()
        self._epd.Clear()

    def _send(self, image) -> None:
        self._epd.display(self._epd.getbuffer(image))
        self._epd.sleep()

    def _clear(self) -> None:
        self._epd.Clear()
        self._epd.sleep()

    def _wake(self) -> None:
        self._epd.init()
        self._epd.Clear()


##
# @brief No-op driver for development/testing, does no hardware I/O
class MockDisplay(Display):

    def __init__(self, width=800, height=480, colors="BW", rot_inv=False) -> None:
        super().__init__(width, height, colors, rot_inv)
        self.last_image_path = None
        self.cleared = False
        self.woke = False

    def display_image(self, path) -> None:
        self.last_image_path = path
        super().display_image(path)

    def _send(self, image) -> None:
        logging.debug("MockDisplay: would render image")

    def _clear(self) -> None:
        self.cleared = True

    def _wake(self) -> None:
        self.woke = True


##
# @brief Build the display driver for the current config/environment
# @note driver="auto" picks MockDisplay off-Pi (e.g. x86_64 dev machine)
# and WaveshareDisplay otherwise. Set driver explicitly to override.
def create_display(type, width, height, colors, rot_inv, driver="auto") -> Display:
    if driver == "mock" or (driver == "auto" and platform.machine() != "aarch64" and platform.machine() != "armv7l"):
        return MockDisplay(width, height, colors, rot_inv)
    return WaveshareDisplay(type, width, height, colors, rot_inv)
