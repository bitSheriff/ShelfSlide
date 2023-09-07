import os
import yaml
import json
import requests
import sys
import random
import subprocess
import logging
import time
import argparse


## own modules
sys.path.append("..")
import src.book as book
import src.display as Display


SLIDESHOW_MIN_SLEEP = 300 # min 5min sleep

##
# @brief Download a cover image from a URL
def download_covers(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any HTTP errors
        with open(path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image: {e}")

##
# @brief Generate a cover filename from the author and title
def generate_coverfilename(author, title):
    author = author.replace(" ", "-").lower()
    title = title.replace(" ", "-").lower()
    return f"{author}_{title}.jpg"

##
# @brief Sort the book list according to the preferred mode
def sort_books(books, mode):
    if mode == "desc":
        books.sort(key=lambda x: x.date, reverse=True)
    elif mode == "asc":
        books.sort(key=lambda x: x.date, reverse=False)
    elif mode == "rand":
        random.shuffle(books)
    else:
        # do nothing
        return books
    newBk = books
    return newBk

##
# @brief Load the book library from a json file
def load_bookLibrary(file, cover_dir, offlineOnly):
    list = []
    for entry in file['read']:
        cover = entry['cover']
        bk = book.Book(entry['title'], entry['author'], cover_dir+"/"+cover['url'], entry['date'])

        # if the book has an online cover, download it, the path needs to be updated
        if (cover['urlType'] == "link") and (not offlineOnly):
                download_covers(cover['url'], cover_dir + "/cache/" + generate_coverfilename(entry['author'], entry['title']))
                bk.set_cover(cover_dir + "/cache/" + generate_coverfilename(entry['author'], entry['title']))
        list.append(bk)
    return list

def config_args():
    parser = argparse.ArgumentParser(description='ShelfSlide')

    parser.add_argument('--offline', '-o', action='store_true', help='Option to run ShelfSlide offline, without downloading covers')
    parser.add_argument('--clear', '-c', action='store_true', help='Just clear the display and exit')

    return parser.parse_args()

##
# @brief Update the book library from a git repository
def update_bookLibrary(book_dir,cover_dir, is_git, slide_mode, offlineOnly):
    if is_git:
        original_directory = os.getcwd()
        os.chdir(book_dir)
        subprocess.run(["git", "pull"])
        os.chdir(original_directory) # change back to original directory
    with open(book_dir+"/books.json",'r') as file:
        books_file = json.load(file)

    book_list = load_bookLibrary(books_file, cover_dir, offlineOnly)
    book_list = sort_books(book_list, slide_mode)
    return book_list

##
# @brief Main function
def main():

    logging.basicConfig(level=logging.DEBUG)

    # configure the arg parser
    parser = config_args()

    # load the config file
    with open('config.yaml', 'r') as file:
            config_file = yaml.safe_load(file)

    # configure the display
    display = Display.display(  config_file['display']['type'],
                                config_file['display']['width'],
                                config_file['display']['height'],
                                config_file['display']['colors'],
                                config_file['display']['rot_inv'])
    
    # check if the clear flag is set
    if parser.clear:
        # clear the display and exit
        display.display_clear()
        sys.exit(0)

    # get the books
    book_list = update_bookLibrary( config_file['books']['dir'],
                                    str(str(config_file['books']['dir']) + "/media"),
                                    config_file['books']['git'],
                                    config_file['slideshow']['mode'],
                                    parser.offline)

    slideshow_sleep = min( config_file['slideshow']['interval'], SLIDESHOW_MIN_SLEEP)

    while True:
        i = 0
        for i in range(len(book_list)):
            display.display_image(book_list[i].get_cover())
            time.sleep(slideshow_sleep)
            display.display_wakeUp()

##
# @brief Main function
if __name__ == "__main__":
    main()