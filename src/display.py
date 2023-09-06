
import os
import sys
from PIL import Image
import epaper
import logging


class display:

    __colors = "BW"
    __type = ""
    __height = 0
    __width = 0
    __epd = None

    # image to display, store it here to avoid reloading it
    __image = None

    def __initEPD(self, type):

        self.__epd = epaper.epaper('epd7in5_V2').EPD()
        self.__epd.init()
        self.__epd.Clear()

    def __init__(self, type) -> None:
        self.__type = type

        # init the e-paper display
        self.__initEPD(type)
        pass

    def __resize_image(self, image):
        image = image.rotate(90, expand=True)
        canvas = Image.new("RGB", (800, 480), "white")

        pic_scale = max( (image.width / 800), (image.height / 480) )

        image = image.resize( (int(image.width//pic_scale), int(image.height//pic_scale)) )

        x_offset = (800 - image.width) // 2
        y_offset = (480 - image.height) // 2
        canvas.paste(image, (x_offset, y_offset))

        return canvas


    def display_image(self, path) -> None:
        # open the image
        logging.debug(f"given image: {path}")
        self.__image = Image.open(path)

        # convert the image to the correct colors
        if self.__colors == "BW":
            self.__image = self.__image.convert(mode="L", dither=Image.FLOYDSTEINBERG)    # TODO "L" or "1", needs to be checked on hardware

        self.__image = self.__resize_image(self.__image)

        self.__epd.display(self.__epd.getbuffer(self.__image))
        self.__epd.sleep()

        pass

    def refresh(self):
        if self.__image == None:
            return
        