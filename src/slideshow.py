import time, sys

sys.path.append("..")
import src.display

# define the update interval in seconds (6h)
UPDATE_INTERVAL = 21600

class slideshow:
    __time = 0
    __book_list = None
    __display = None
    __timestamp = 0
    __current_book = 0

    interrupt_update = False
    __last_update = 0

    def __init__(self, period, book_list, display) -> None:
        self.__time = period
        self.__book_list = book_list
        self.__display = display
        self.__last_update = time.time()
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

        # check if the update interval has passed
        if ((time.time() - self.__last_update) > UPDATE_INTERVAL):
            # update the last update timestamp
            self.__last_update = time.time()
            self.interrupt_update = True

        pass

    def update_done(self, book_list) -> None:
        # update the book list
        self.__book_list = book_list
        # reset the update flag
        self.interrupt_update = False
        self.__current_book = 0
        pass