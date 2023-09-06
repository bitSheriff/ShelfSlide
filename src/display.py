
import os
import sys
from PIL import Image
import epaper
import src.epdDriver as epdDriver
import logging

USE_OWN_DRIVER = 0

class display:

    __colors = "BW"
    __type = ""
    __height = 0
    __width = 0
    __epd = None

    # image to display, store it here to avoid reloading it
    __image = None

    def __initEPD(self, type):

        if USE_OWN_DRIVER:
            self.__epd = epdDriver.EPD()
        else:
            self.__epd = epaper.epaper('epd7in5_V2').EPD()

        self.__epd.init()

        if not USE_OWN_DRIVER:
            self.__epd.Clear()

    def __init__(self, type) -> None:
        self.__type = type

        # init the e-paper display
        self.__initEPD(type)
        pass

    def __resize_image(self, image):
        image = image.rotate(90)
        new_size = (800, 480)

        #image.thumbnail(new_size)  # Use Image.ANTIALIAS for high-quality resizing

        image = image.resize(new_size)

        image.save("test.jpg")

        return image



    def display_image(self, path) -> None:
        # open the image
        logging.debug(f"given image: {path}")
        self.__image = Image.open(path)

        if not USE_OWN_DRIVER:
            # convert the image to the correct colors
            if self.__colors == "BW":
               self.__image = self.__image.convert(mode="L", dither=Image.FLOYDSTEINBERG)    # TODO "L" or "1", needs to be checked on hardware


        self.__image = self.__resize_image(self.__image)

        if USE_OWN_DRIVER:
            self.__epd.display_frame(self.__epd.get_frame_buffer(self.__image))
        else:
            self.__epd.display(self.__epd.getbuffer(self.__image))
            self.__epd.sleep()

        pass

    def refresh(self):
        if self.__image == None:
            return
        