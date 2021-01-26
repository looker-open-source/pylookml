import pathlib
from urllib.parse import urlparse

class url(object):
    def __init__(self,url):
        self.url = urlparse(url)
    def with_port_if_exists(self): 
        return f"{self.url.scheme}://{self.url.hostname}{ ':'+str(self.url.port) if self.url.port else ''}"
    def with_no_port(self): return f"{self.url.scheme}://{self.url.hostname}"

class path(object):
    pass