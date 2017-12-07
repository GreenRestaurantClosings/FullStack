import os

REPO_NAME = "FullStack"
DEBUG = True

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def parent_dir(path):
    return os.path.abspath(os.path.join(path, os.pardir))

PROJECT_ROOT = parent_dir(APP_DIR)
FREEZER_DESTINATION = PROJECT_ROOT

FREEZER_BASE_URL = "http://localhost/{0}".format(REPO_NAME)
FREEZER_REMOVE_EXTRA_FILES = False