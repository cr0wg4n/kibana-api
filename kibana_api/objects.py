import json
import secrets
import os
from .base import BaseModel, Utils

class Space(BaseModel):
    def __init__(self, id=None, name=None, description=None, color=None, initials=None, disabledFeatures=None, _reserved=None, kibana=None) -> None:
        super().__init__(["id", "name","description", "color", "initials", "disabledFeatures", "_reserved"], kibana=kibana)
        self.create_url = "api/spaces/space"
        self.all_url = self.create_url
        self.id = id
        self.name = name
        self.description = description
        self.color = color
        self.initials = initials
        self.disabledFeatures = disabledFeatures
        self._reserved = _reserved

    def create(self):
        url = self.url(self.create_url)
        data = self.serialize()
        response = self.requester(url=url, method="post", data=data)
        return response

    def all(self):
        url = self.url(self.create_url)
        response = self.requester(url=url, method="get")
        return response
        
class Object(BaseModel):
    def __init__(self, space_id=None, kibana=None, attribs={}, type="", references={}) -> None:
        super().__init__([], space_id=space_id, kibana=kibana)
        self.types =["visualization", "dashboard", "search", "index-pattern", 
        "config", "timelion-sheet", "url", "query", "canvas-element", "canvas-workpad", "lens",
        "infrastructure-ui-source", "metrics-explorer-view", "inventory-view"]
        self.create_url = "api/saved_objects"
        self.import_url = "api/saved_objects/_import"
        self.all_url = "api/saved_objects/_find"
        self.get_url = "api/saved_objects"
        self.attribs = attribs
        self.references = references
        self.type = type.lower()

    def get(self, id, type=""):
        type = self.type if not type else type.lower()
        if not self.validate_type(type, types=self.types):
            return None
        url = self.url(self.get_url, type, id)
        return self.requester(url=url, method="get")

    def all(self, type=""):
        params = {
            "type": self.types if not type else type
        }
        url = self.url(self.all_url)
        return self.requester(url=url, method="get", params=params)

    def create(self, type="", attribs={}, references={}, body={}):
        type = (self.type if not type else type.lower())
        attribs = (self.attribs if not attribs else attribs)
        references = (self.references if not references else references)
        if not self.validate_type(type, types=self.types):
            return None
        url = self.url(self.create_url, type)
        data = {}
        if attribs:
            data["attributes"] = attribs
        if references:
            data["references"] = references
        data = data if not body else body
        response = self.requester(url=url, method="post", data=json.dumps(data))
        return response

    def loads(self, file):
        url = self.url(self.import_url)
        response = self.requester(url=url, method="post", files={"file": file})
        return response

    def dumps(self):
        pass

class Panel():
    def __init__(self, panel_name, width, height, pos_x, pos_y, id=None, visualization_id= "") -> None:
        self.id = self.__random_string() if not id else id
        self.panel_name = panel_name
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.visualization_id=visualization_id

    def __random_string(self):
        return secrets.token_urlsafe(32)

    def create(self):
        return {
            "version": "7.8.0",
            "gridData": {
                "x": self.pos_x,
                "y": self.pos_y,
                "w": self.width,
                "h": self.height,
                "i": self.id
            },
            "panelIndex": self.id,
            "embeddableConfig": {},
            "panelRefName": self.panel_name
        }

    def get_reference(self):
        return {} if not self.visualization_id else {
            "name": self.panel_name,
            "type": "visualization",
            "id": self.visualization_id
        }

class Dashboard():
    def __init__(self, title, panels=[], references=[], query="") -> None:
        self.primitive_type="dashboard"
        self.title = title
        self.panels = panels
        self.references = references
        self.query=query

    def create(self):
        return {
            "attributes": {
                "title": self.title,
                "hits": 0,
                "description": "",
                "panelsJSON": json.dumps(self.panels),
                "optionsJSON": "{\"useMargins\":true,\"hidePanelTitles\":false}",
                "version": 1,
                "timeRestore": False,
                "kibanaSavedObjectMeta": {
                    "searchSourceJSON": self.__querier()
                }
            },
            "references": self.references
        }
        
    def __querier(self):
        data = {
            "query": {
                "query": self.query,
                "language": "kuery"
            },
            "filter": []
        }
        return json.dumps(data)
    
class Visualization(Utils):
    
    def __init__(self, index_pattern_id:str, title:str="", query:str="", mappings_dir_path:str=None, type:str="") -> None:
        CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        self.primitive_type="visualization"
        self.types=["area", "heatmap", "line", "metric", "pie", "table", "tagcloud"]
        self.type= type.lower()
        self.title = title
        self.index_pattern_id = index_pattern_id
        self.query = query
        self.mappings_dir_path = os.path.join(CURRENT_DIR, 'mappings') if not mappings_dir_path else mappings_dir_path
        self.data = self.load_visualizations()

    def load_visualizations(self):
        data = {}
        for type in self.types:
            file_path =  os.path.join(self.mappings_dir_path, "{}.json".format(type))
            data[type] = self.__read_json_file(file_path)
        return data

    def create(self, index_pattern_id:str=None, title:str="", body={}, query:str="") :
        title = self.title if not title else title
        visualization_state = self.__templater(title) if not body else self.__templater_json(title, body) 
        search_state = self.__querier(self.query if not query else query)
        index_pattern_id = self.index_pattern_id if not index_pattern_id else index_pattern_id
        return {
            "attributes": {
                "title": title,
                "visState": visualization_state,
                "uiStateJSON": "{}",
                "description": "",
                "version": 1,
                "kibanaSavedObjectMeta": {
                    "searchSourceJSON": search_state
                }
            },
            "references": [{
                "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
                "type": "index-pattern",
                "id": index_pattern_id
            }]
        }

    def __read_json_file(self, file_path):
        file = open(file_path, 'r')
        read = file.read()
        file.close()
        return json.loads(read)

    def __templater_json(self, title, _json) -> str:
        data = _json
        data["title"] = title
        return json.dumps(data)

    def __templater(self, title) -> str:
        if self.validate_type(self.type, self.types):
            data = self.data[self.type]
            data["title"] = title
            return json.dumps(data)

    def __querier(self, query=None) -> str:
        data = {
            "query": {
                "query": query,
                "language": "kuery"
            },
            "indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index",
            "filter": []
        }
        return json.dumps(data)



# class TooLargePanel(Exception):
#     def __init__(self, *args: object) -> None:
#         super().__init__(*args)

