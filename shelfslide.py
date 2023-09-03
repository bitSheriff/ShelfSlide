import os
import yaml
import json
import requests


def download_covers(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any HTTP errors

        with open(path, 'wb') as file:
            file.write(response.content)

        print(f"Image downloaded successfully to {path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image: {e}")

def generate_coverfilename(author, title):
    author = author.replace(" ", "-").lower()
    title = title.replace(" ", "-").lower()
    return f"{author}_{title}.jpg"

##
# @brief Main function
if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config_file = yaml.safe_load(file)

    print(config_file['books']['dir'])

    books_dir = str(str(config_file['books']['dir']) + "/books.json")
    cover_dir = str(str(config_file['books']['dir']) + "/media")

    with open(books_dir,'r') as file:
        books_file = json.load(file)

    for book in books_file['read']:
        print(book)
        cover = book['cover']
        if cover['urlType'] == "link":
                download_covers(cover['url'], cover_dir + "/cache/" + generate_coverfilename(book['author'], book['title']))