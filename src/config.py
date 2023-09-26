

def copy_conf():
    """
    Copy the configuration file to the user's home directory.
    """
    import os
    import shutil
    from . import __file__ as root

    root = os.path.dirname(root)
    conf = os.path.join(root, 'config.yaml')
    home = os.path.expanduser('~')
    dest = os.path.join(home, '.config', 'shelfslide', 'config.yaml')

    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))

    shutil.copy(conf, dest)
    print("Configuration file copied to {}".format(dest))

def copy_books_dir():
    """
    Copy the books directory to the user's home directory.
    """
    import os
    import shutil
    from . import __file__ as root

    root = os.path.dirname(root)
    books = os.path.join(root, 'books')
    home = os.path.expanduser('~')
    dest = os.path.join(home, '.config', 'shelfslide', 'books')

    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))

    shutil.copytree(books, dest)
    print("Books directory copied to {}".format(dest))