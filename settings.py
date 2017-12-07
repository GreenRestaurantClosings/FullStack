import os

REPO_NAME = "FULL STACK"
DEBUG = True

APP_DIR = os.path.dirname(os.path.abspath(__file__)) #add

def parent_dir(path):
    return os.path.abspath(os.join(path, os.pardir))

PROJECT_ROOT = parent_dir(APP_DIR)

FREEZER_DESTINATION = PROJECT_ROOT

FREEZER_BASE_URL = "https://greenrestaurantclosings.github.io/FullStack/".format(REPO_NAME)

FREEZER_REMOVE_EXTRA_FILES = False

FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
FLATPAGES_ROOT = os.path.join(APP_DIR, 'pages')
FLATPAGES_EXTENSION = '.md'
