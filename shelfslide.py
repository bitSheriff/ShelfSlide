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
import glob

## own modules
sys.path.append("..")
import src.book as Book
import src.display as Display
import src.slideshow as Slideshow

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
# Check if the cover was already downloaded once
def cover_exists(name, dir):
    files = glob.glob(dir+name)
    print(f"{dir}, {name}, {len(files)}")
    if len(files) == 0:
        return False
    else:
        return True

##
# @brief Load the book library from a json file
def load_bookLibrary(file, cover_dir, offlineOnly):
    list = []
    for entry in file['read']:
        cover = entry['cover']
        bk = Book.Book(entry['title'], entry['author'], cover_dir+"/"+cover['url'], entry['date'])

        # if the book has an online cover, download it, the path needs to be updated
        if (cover['urlType'] == "link") and (not offlineOnly):
                # check if the file should be downloaded
                if not cover_exists(generate_coverfilename(entry['author'], entry['title']), cover_dir + "/cache/"):
                    download_covers(cover['url'], cover_dir + "/cache/" + generate_coverfilename(entry['author'], entry['title']))
                bk.set_cover(cover_dir + "/cache/" + generate_coverfilename(entry['author'], entry['title']))
        list.append(bk)
    return list

##
# @brief Configure the argument parser
def config_args():
    parser = argparse.ArgumentParser(prog='ShelfSlide',
                                     description='Show your read books on an e-paper display',
                                     epilog='For more information please visit github.com/bitSheriff/ShelfSlide')

    parser.add_argument('--offline', '-o', action='store_true', help='Option to run ShelfSlide offline, without downloading covers')
    parser.add_argument('--clear',   '-c', action='store_true', help='Just clear the display and exit')
    parser.add_argument('--time',    '-t', default=0,           help='Time between slides in seconds')
    parser.add_argument('--dryrun',  '-d', action='store_true', help='Dry run, test if all given links are valid')
    parser.add_argument('--update',  '-u', action='store_true', help='Update the application from the git repository')
    parser.add_argument('--verbose', '-v', action='store_true', help='Log all happenings')


    # return the parsed arguments
    return parser.parse_args()

##
# Clean the downloaded covers
def clean_cache(cover_dir):
    path = cover_dir + "/cache/"
    
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def file_is_media(path):
    media_extensions = ["jpeg", "jpg", "png"]

    # check if the extension is one of the allowed one
    for ext in media_extensions:
        if ext in path:
            return True
    # extension not found, so no allowed media file
    return False


def load_simple_bookLibrary(cover_dir):
    book_list = []

    for file in os.listdir(cover_dir):
        file_path = os.path.join(cover_dir, file)
        if file_is_media(file_path):
            bk = Book.Book(title = "", author = "", cover = file_path, date = "")
            book_list.append(bk)
    return book_list

##
# @brief Update the book library from a git repository
def update_bookLibrary(book_dir,cover_dir, is_git, slide_mode, offlineOnly, clean, simpleMode):
    if is_git:
        original_directory = os.getcwd()
        os.chdir(book_dir)
        subprocess.run(["git", "pull"])
        os.chdir(original_directory) # change back to original directory

    if simpleMode:
        return load_simple_bookLibrary(cover_dir)

    with open(book_dir+"/books.json",'r') as file:
        books_file = json.load(file)

    # check if the old covers should be removed before downloading the new
    if clean:
        clean_cache(cover_dir)

    book_list = load_bookLibrary(books_file, cover_dir, offlineOnly)
    book_list = sort_books(book_list, slide_mode)
    return book_list

def error_exit(display, text):
        logging.error(text)
        display.display_logo()
        sys.exit(0)

##
# @brief Main function
def main():

    # configure the arg parser
    parser = config_args()

    if parser.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    # load the config file
    with open('config.yaml', 'r') as file:
            config_file = yaml.safe_load(file)

    # configure the display
    display = Display.display(  config_file['display']['type'],
                                config_file['display']['width'],
                                config_file['display']['height'],
                                config_file['display']['colors'],
                                config_file['display']['rot_inv'])
    


    # check if the update flag is set 
    if parser.update:
        subprocess.run(["git", "pull"])
        print("Updated ShelfSlide\n Please restart the application")
        error_exit(display)

    # check if the dryrun flag is set
    if parser.dryrun:
        raise NotImplementedError("Dry run not implemented yet")

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
                                    parser.offline,
                                    config_file['books']['clean'],
                                    config_file['books']['simpleMode'])

    slideshow_sleep = min( config_file['slideshow']['interval'], SLIDESHOW_MIN_SLEEP)

    # override the configured tme if the user specified one (allowed to be less than 5min)
    if parser.time != 0:
        slideshow_sleep = parser.time

    # init the slideshow
    slideshow = Slideshow.slideshow(int(slideshow_sleep), book_list, display)

    # main part of the application
    while True:
        # run the slideshow
        slideshow.run()

##
# @brief Main function
if __name__ == "__main__":
    main()