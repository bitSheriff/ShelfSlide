
import os
import sys
from PIL import Image
from epaper import *

class display:

    __colors = ""
    __type = ""
    __height = 0
    __width = 0
    __epd = None

    # image to display, store it here to avoid reloading it
    __image = None

    def __initEPD(self, type):
        if type == "epd7in5":
            self.__epd = epaper.epaper('epd7in5').EPD()
        

    def __init__(self, type) -> None:
        self.__type = type

        # init the e-paper display
        self.__initEPD(type)
        pass


    def display_image(self, path) -> None:
        # open the image
        self.__image = Image.open(path)

        # convert the image to the correct colors
        if self.__colors == "BW":
            self.__image = self.__image.convert(mode="L", dither=Image.FLOYDSTEINBERG)    # TODO "L" or "1", needs to be checked on hardware

        pass

    def refresh(self):
        if self.__image == None:
            return
        