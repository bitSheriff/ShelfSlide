import os
import yaml
import json
import requests
import sys
import random
import subprocess

## own modules
sys.path.append("..")
import src.book as book

##
# @brief Download a cover image from a URL
def download_covers(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any HTTP errors
        with open(path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

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
        return books.sort(key=lambda x: x.date, reverse=True)
    elif mode == "asc":
        return books.sort(key=lambda x: x.date, reverse=False)
    elif mode == "rand":
        return random.shuffle(books)
    else:
        # do nothing
        return books

##
# @brief Load the book library from a json file
def load_bookLibrary(file, cover_dir):
    list = []
    for entry in file['read']:
        cover = entry['cover']
        bk = book.Book(entry['title'], entry['author'], entry['cover'], entry['date'])

        # if the book has an online cover, download it, the path needs to be updated
        if cover['urlType'] == "link":
                download_covers(cover['url'], cover_dir + "/cache/" + generate_coverfilename(entry['author'], entry['title']))
                bk.set_cover(cover_dir + "/cache/" + generate_coverfilename(entry['author'], entry['title']))
        list.append(bk)
    return list

##
# @brief Update the book library from a git repository
def update_bookLibrary(book_dir, is_git):
    if is_git:
        original_directory = os.getcwd()
        os.chdir(book_dir)
        subprocess.run(["git", "pull"])
        os.chdir(original_directory) # change back to original directory


##
# @brief Main function
if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config_file = yaml.safe_load(file)

    books_dir = str(str(config_file['books']['dir']) + "/books.json")
    cover_dir = str(str(config_file['books']['dir']) + "/media")

    update_bookLibrary(config_file['books']['dir'], config_file['books']['git'])

    with open(books_dir,'r') as file:
        books_file = json.load(file)

    book_list = load_bookLibrary(books_file, cover_dir)

    print(*book_list)
    bk = sort_books(book_list, config_file['slideshow']['mode'])
    print(*book_list)