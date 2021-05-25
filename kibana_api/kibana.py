import requests
from urllib.parse import urljoin
from .objects import Space, Object

spaces = "http://localhost:5601/api/spaces/space"
host = 'http://localhost:5601/s/demo/api/saved_objects/index-pattern'

class Kibana:
    def __init__(self, base_url, username=None, password=None) -> None:
        self.base_url = base_url
        self.username = username
        self.password = password

    def url(self, *args) -> str:
        url = self.base_url
        for arg in args:
            if arg:
                url = urljoin(url, arg + "/")
        return  url[:-1] if url[-1:]=="/" else url

    def requester(self, **kwargs): 
        headers = {
            "Content-Type": "application/json",
            "kbn-xsrf": "True",
        } if not "files" in kwargs else {
            "kbn-xsrf": "True",
        }
        auth = (self.username, self.password) if (self.username and self.password) else None
        return requests.request(headers=headers, auth=auth, **kwargs)

    def space(self, **kwargs):
        return Space(kibana=self, **kwargs)

    def object(self, **kwargs): 
        return Object(kibana=self, **kwargs)
