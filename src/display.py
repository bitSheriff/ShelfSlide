
import os, sys, platform
from PIL import Image
import epaper
import logging


if platform.machine() == "x86_64": # Dev machine, use stub
    import gpiozero
    from gpiozero.pins.mock import MockFactory
    gpiozero.Device.pin_factory = MockFactory()
else: # Raspberry Pi
    import RPi.GPIO as GPIO

KNOWN_EPDs = ["epd7in5_V2"]
IMAGE_LIB = "pillow" # "opencv" (not ready for usage) / "pillow"

class display:

    __colors = "BW"
    __type = "epd7in5_V2"
    __height = 480
    __width = 800
    __epd = None
    __rot = 90

    # image to display, store it here to avoid reloading it
    __image = None

    def __initEPD(self):

        if not self.__type in KNOWN_EPDs:
            raise NotImplementedError("NOT SUPPORTED EPD")

        GPIO.setmode(GPIO.BCM)

        self.__epd = epaper.epaper(self.__type).EPD()
        self.__epd.init()
        self.__epd.Clear()

    def __init__(self, type, w, h, c, rot_inv) -> None:
        # init the private variables
        self.__type = type
        self.__width = w
        self.__height = h
        self.__colors = c

        # init the e-paper display
        self.__initEPD()

        # rotate the cover in the opposite direction
        if rot_inv:
            self.__rot = -90
        pass

    def __resize_image(self, image):
        image = image.rotate(self.__rot, expand=True)
        canvas = Image.new("RGB", (self.__width, self.__height), "white")

        pic_scale = max( (image.width / self.__width), (image.height / self.__height) )

        image = image.resize( (int(image.width//pic_scale), int(image.height//pic_scale)) )

        x_offset = (self.__width - image.width) // 2
        y_offset = (self.__height - image.height) // 2
        canvas.paste(image, (x_offset, y_offset))

        return canvas

    def __convert_colors(self, path):

        if IMAGE_LIB == "opencv":
            import cv2
            image = cv2.imread(path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return image
        else:
            image = Image.open(path)
            image = image.convert(mode="L")
            return image



    def display_image(self, path) -> None:
        
        # convert the image to the correct colors
        if self.__colors == "BW":
            self.__image = self.__convert_colors(path)

        self.__image = self.__resize_image(self.__image)

        # send the image and set the device sleeping
        self.__epd.display(self.__epd.getbuffer(self.__image))
        self.__epd.sleep()
        pass

    def display_wakeUp(self) -> None:
            self.__epd.init()
            self.__epd.Clear()

    def display_clear(self) -> None:
        self.__epd.Clear()
        self.__epd.sleep()

    def display_logo(self) -> None:
        self.display_image("doc/logo.jpeg")

    def refresh(self):
        if self.__image == None:
            return
        