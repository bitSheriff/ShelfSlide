import time, sys

sys.path.append("..")
import src.display


class slideshow:
    __time = 0
    __book_list = None
    __display = None
    __timestamp = 0
    __current_book = 0

    def __init__(self, time, book_list, display) -> None:
        self.__time = time
        self.__book_list = book_list
        self.__display = display
        pass

    def run(self) -> None:
        # check if it is time for the next book
        if ((time.time() - self.__timestamp) > self.__time):
            # update the timestamp and the current book
            self.__timestamp = time.time()
            self.__current_book = (self.__current_book + 1) % len(self.__book_list)
            
            # display the next book
            self.__display.display_wakeUp()
            self.__display.display_image(self.__book_list[self.__current_book].get_cover())
        pass