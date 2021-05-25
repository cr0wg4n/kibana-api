import json
import secrets
import os
from .base import BaseModel

class Space(BaseModel):
    def __init__(self, id=None, name=None, description=None, color=None, initials=None, disabledFeatures=None, _reserved=None, kibana=None) -> None:
        super().__init__(["id", "name","description", "color", "initials", "disabledFeatures", "_reserved"], kibana=kibana)
        self.create_url = "api/spaces/space"
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

class Object(BaseModel):
    def __init__(self, space_id=None, kibana=None, attribs={}, type=None, references={}) -> None:
        super().__init__([], space_id=space_id, kibana=kibana)
        self.types =["visualization", "dashboard", "search", "index-pattern", 
        "config", "timelion-sheet", "url", "query", "canvas-element", "canvas-workpad", "lens",
        "infrastructure-ui-source", "metrics-explorer-view", "inventory-view"]
        self.create_url = "api/saved_objects"
        self.import_url = "api/saved_objects/_import"
        self.all_url = "api/saved_objects/_find"
        self.attribs = attribs
        self.references = references
        self.type = type

    def all(self, type=None):
        params = {
            "type": self.types if not type else type
        }
        url = self.url(self.all_url)
        return self.requester(url=url, method="get", params=params)

    def create(self, type=None, attribs={}, references={}, body={}):
        type = (self.type.lower() if self.type else type.lower())
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
    
class Visualization():
    
    def __init__(self, type, title, index_pattern_id, query="", mappings_filepath=None) -> None:
        CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        MAPPINGS_DIR = os.path.join(CURRENT_DIR, 'mappings')
        print("mapping_dir", MAPPINGS_DIR)
        self.primitive_type="visualization"
        self.type= type
        self.title = title
        self.index_pattern_id = index_pattern_id
        self.query = query
        self.mappings_file_path = os.path.join(MAPPINGS_DIR, "{}.json".format(self.type)) if not mappings_filepath else mappings_filepath

    def create(self):
        return {
            "attributes": {
                "title": self.title,
                "visState": self.__templater(self.title),
                "uiStateJSON": "{}",
                "description": "",
                "version": 1,
                "kibanaSavedObjectMeta": {
                    "searchSourceJSON": self.__querier()
                }
            },
            "references": [{
                "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
                "type": "index-pattern",
                "id": self.index_pattern_id
            }]
        }

    def __templater(self, title):
        file = open(self.mappings_file_path, 'r')
        data = json.load(file)
        data["title"] = title
        file.close()
        return json.dumps(data)

    def __querier(self):
        data = {
            "query": {
                "query": self.query,
                "language": "kuery"
            },
            "indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index",
            "filter": []
        }
        return json.dumps(data)



# class TooLargePanel(Exception):
#     def __init__(self, *args: object) -> None:
#         super().__init__(*args)

