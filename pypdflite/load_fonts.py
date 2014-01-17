import os
import string
from sys import platform as _platform
import shutil
import pickle

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
FONT_DIR = os.path.join(PROJECT_DIR, 'fonts')

MAC_SEARCH_PATH = '/Library/Fonts/'
WINDOWS_SEARCH_PATH = "C:\\Windows\\Fonts:"
LINUX_SEACH_PATH = 'usr/share/fonts/truetype'
SEARCH_PATH = None

english = 'abcdefghijklmnopqrstuvwxyz'


def get_ttf():
    """ Given a search path, find file with requested extention """
    font_dict = {}
    families = []
    for path in string.split(SEARCH_PATH, os.pathsep):
        path = os.path.expanduser(path)
        for item in os.listdir(path):
            root, ext = os.path.splitext(item)
            if ext == '.ttf':
                if root[0].lower() in english:
                    source = os.path.join(path, item)
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


def main():
    # Check for system, guess path of fonts
    mypath = raw_input("Type font path, or [enter] to use system fonts > ")
    global SEARCH_PATH
    if mypath == '':
        if _platform == "linux" or _platform == "linux2":
            SEARCH_PATH = LINUX_SEACH_PATH
        elif _platform == "darwin":
            SEARCH_PATH = MAC_SEARCH_PATH
        elif _platform == "win32":
            SEARCH_PATH = WINDOWS_SEARCH_PATH
        else:
            print "platform not recognised"
    else:
        SEARCH_PATH = mypath

    font_dict, families = get_ttf()

    font_dict['font_families'] = families

    pickle.dump(font_dict, open(os.path.join(FONT_DIR, 'font_dict.p'), 'wb'))


if __name__ == '__main__':
    main()
