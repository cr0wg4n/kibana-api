import json
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
    def __init__(self, space_id=None, kibana=None, _json={}, type=None) -> None:
        super().__init__([], space_id=space_id, kibana=kibana)
        self.types =["visualization", "dashboard", "search", "index-pattern", "config", "timelion-sheet"]
        self.create_url = "api/saved_objects"
        self.import_url = "api/saved_objects/_import"
        self._json = _json
        self.type = type

    def create(self, type=None, _json=None):
        type = (self.type.lower() if self.type else type.lower())
        _json = (self._json if self._json else _json)
        
        if not (self.validate_type(type, types=self.types) and type and _json):
            return None
        url = self.url(self.create_url, type)
        data = {
            "attributes": {
                **_json
            }
        }
        response = self.requester(url=url, method="post", data=json.dumps(data))
        return response

    def loads(self, file):
        url = self.kibana.url(self.import_url)
        response = self.requester(url=url, method="post", files={"file": file})
        return response

    def dumps(self):
        pass
