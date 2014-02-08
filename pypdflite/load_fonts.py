import os
import string
import errno
from sys import platform as _platform
import shutil
import pickle
import itertools

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
    rootdirlist = string.split(SEARCH_PATH, os.pathsep)

    for rootdir in rootdirlist:
        rootdir = os.path.expanduser(rootdir)

    for dirName, subdirList, filelist in itertools.chain.from_iterable(os.walk(path) for path in rootdirlist):
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


def remove_fonts():
    try:
        for ffile in os.listdir(FONT_DIR):
            os.remove(os.path.join(FONT_DIR, ffile))
        os.rmdir(FONT_DIR)
    except OSError as exception:
        if exception.errno != errno.ENOENT:
            raise


def load_fonts(search_path=None):
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

    if search_path is not None:
        SEARCH_PATH += os.pathsep + search_path

    font_dict, families = get_ttf()

    font_dict['font_families'] = families

    pickle.dump(font_dict, open(os.path.join(FONT_DIR, 'font_dict.p'), 'wb'))


def load_font_files(filelist):
    for ffile in filelist:
        shututil.copy(ffile, FONT_DIR)

    self.load_fonts(FONT_DIR)

if __name__ == '__main__':
    load_fonts()
