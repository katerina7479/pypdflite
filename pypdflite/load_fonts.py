import os
import string
import errno
from sys import platform as _platform
import shutil
import pickle

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
FONT_DIR = os.path.join(PROJECT_DIR, 'fonts')

MAC_SEARCH_PATH = '/Library/Fonts/'
WINDOWS_SEARCH_PATH = "C:\\Windows\\Fonts"
LINUX_SEARCH_PATH = '/usr/share/fonts'
SEARCH_PATH = None

english = 'abcdefghijklmnopqrstuvwxyz'


def get_ttf():
    """ Given a search path, find file with requested extention """
    font_dict = {}
    families = []
    for rootdir in string.split(SEARCH_PATH, os.pathsep):
        rootdir = os.path.expanduser(rootdir)
        for dirName, subdirList, filelist in os.walk(rootdir):
            for item in filelist:
                root, ext = os.path.splitext(item)
                if ext == '.ttf':
                    if root[0].lower() in english:
                        source = os.path.join(dirName, item)
                        name = root.lower()
                        if ' bold' in name:
                            name = name.replace(' bold', '_bold')
                            if ' italic' in name:
                                name = name.replace(' italic', '_italic')
                        elif 'bold' in name:
                            name = name.replace('bold', '_bold')
                            if 'italic' in name:
                                name = name.replace('italic', '_italic')
                        elif ' italic' in name:
                            name = name.replace(' italic', '_italic')
                        elif 'italic' in name:
                            name = name.replace('italic', '_italic')
                        elif 'oblique' in name:
                            name = name.replace('oblique', '_italic')
                        else:
                            families.append(name)
                        font_dict[name] = source

    return font_dict, families


def load_fonts():
    # Check for system, guess path of fonts
    try:
        os.makedirs(FONT_DIR)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    global SEARCH_PATH
    if _platform == "linux" or _platform == "linux2":
        SEARCH_PATH = LINUX_SEARCH_PATH
    elif _platform == "darwin":
        SEARCH_PATH = MAC_SEARCH_PATH
    elif _platform == "win32":
        SEARCH_PATH = WINDOWS_SEARCH_PATH
    else:
        SEARCH_PATH = raw_input("Type path to fonts, then enter. > ")

    font_dict, families = get_ttf()

    font_dict['font_families'] = families

    pickle.dump(font_dict, open(os.path.join(FONT_DIR, 'font_dict.p'), 'wb'))


def check_fonts_loaded():
    if os.path.exists(os.path.join(FONT_DIR, 'font_dict.p')):
        pass
    else:
        load_fonts()

if __name__ == '__main__':
    check_fonts_loaded()
