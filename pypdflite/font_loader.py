import os
import string
from sys import platform as _platform
import itertools


MAC_SEARCH_PATH = '/Library/Fonts/'
WINDOWS_SEARCH_PATH = "C:\\Windows\\Fonts"
LINUX_SEARCH_PATH = '/usr/share/fonts'

english = 'abcdefghijklmnopqrstuvwxyz'

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Font_Loader(object):
    __metaclass__ = Singleton

    def __init__(self, search_path=None):
        self.search_path = search_path

    def get_ttf(self):
        """ Given a search path, find file with requested extention """
        font_dict = {}
        families = []
        rootdirlist = string.split(self.search_path, os.pathsep)

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

        self.font_dict = font_dict
        self.families = families

    def load_fonts(self):
        if self.search_path is None:
            if _platform == "linux" or _platform == "linux2":
                self.search_path = LINUX_SEARCH_PATH
            elif _platform == "darwin":
                self.search_path = MAC_SEARCH_PATH
            elif _platform == "win32":
                self.search_path = WINDOWS_SEARCH_PATH

        self.get_ttf()

    def load_from_dir(self, directory):
        self.search_path = directory
        self.load_fonts()

    def load_from_list(self, filelist):
        self.search_path = filelist[0]
        for ffile in filelist[1:]:
            self.search_path += os.pathsep + ffile
        self.load_fonts()


Font_Loader = Font_Loader()
