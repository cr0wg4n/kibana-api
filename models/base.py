from multipledispatch import dispatch
import json

class BaseModel:
    def __init__(self, attributes, space_id=None, kibana=None, _json=None) -> None:
        self.attributes = attributes
        self.space_id = "" if not space_id else f's/{space_id}'
        self.kibana = kibana
        self._json = _json

    def deserialize(self, _json):
        data = json.loads(_json)
        [self.validate_value(self, data, attrib) for attrib in self.attributes]
        return self

    def serialize(self):
        data = {}
        object = self.__dict__
        [self.validate_value(data, object, attrib) for attrib in self.attributes]
        return json.dumps(data)
    
    @dispatch(dict, dict, str)
    def validate_value(self, target_object, object, attribute):
        if object.get(attribute):
            target_object[attribute] = object[attribute]
            return target_object
    
    @dispatch(object, dict, str)
    def validate_value(self, target_object, object, attribute):
        if object.get(attribute):
            setattr(target_object, attribute, object[attribute])
            return target_object

    def validate_type(self, value, types):
        return value in types

    def requester(self, **kwargs):
        return self.kibana.requester(**kwargs)

    def url(self, *args):
        return self.kibana.url(self.kibana.base_url, self.space_id, *args)