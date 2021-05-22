import random
from requests.api import request
from models.kibana import Kibana
import unittest


URL = "http://localhost:5601"
USERNAME = ""
PASSWORD = ""

class TestStringMethods(unittest.TestCase):

    def test_url_parser(self):
        pass
        kibana = Kibana(base_url=URL)
        url = kibana.url(URL, "1", "2", "3")
        self.assertEqual("http://localhost:5601/1/2/3", url)

    def test_create_space(self):
        kibana = Kibana(base_url=URL)
        id = f"test-{int(random.randint(0,100)*0.33)}"
        name = "test" + id
        description = "descripcion del espacio de pruebas"
        color = "#000000"
        response = kibana.space(id=id, name=name, description=description, color=color).create()
        response_json = {
            "id": id,
            "name": name,
            "description": description,
            "color": color,
            "disabledFeatures": []
        }
        self.assertEqual(response.json(), response_json)

    def test_create_object(self):
        kibana = Kibana(base_url=URL)
        pattern_json = {
            "title":"demo*",
            "timeFieldName": "@timestamp",
            "fields":"[]"
        }
        res = kibana.object(space_id="demo", _json=pattern_json).create('index-pattern')
        self.assertEqual(res.json()["attributes"], pattern_json)

    def test_import(self):
        pass
        # kibana = Kibana(base_url=URL)

if __name__ == "__main__":
    unittest.main()