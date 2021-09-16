import pathlib
from urllib.parse import urlparse
import configparser
import os
from pathlib import Path
class url(object):
    def __init__(self,url):
        self.url = urlparse(url)
    def with_port_if_exists(self): 
        return f"{self.url.scheme}://{self.url.hostname}{ ':'+str(self.url.port) if self.url.port else ''}"
    def with_no_port(self): return f"{self.url.scheme}://{self.url.hostname}"

class path(object):
    pass

class Conf(object):
    def __init__(self, config=None):
        self.conf = configparser.ConfigParser()
        home = str(Path.home())
        if config:
            self.conf.read(config)
        elif os.path.exists(f'{home}/pylookml.ini'):
            self.conf.read(f'{home}/pylookml.ini')
        elif os.path.exists(f'{home}/.pylookml'):
            self.conf.read(f'{home}/.pylookml')
        elif os.path.exists('.pylookml'):
            self.conf.read('.pylookml')
        elif os.path.exists('pylookml.ini'):
            self.conf.read('pylookml.ini')
        else:
            raise Exception('''pylookml.ini not found. Please add to ~/pylookml.ini or add pylookml.ini to the current working directory.
            file can also be named .pylookml to remain hidden
            ''')