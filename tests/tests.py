from kibana_api import Dashboard, Panel, Visualization, Kibana
import random
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
        pass
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

    def test_create_index_pattern(self):
        pass
        pattern_json = {
            "title":"demo*",
            "timeFieldName": "@timestamp",
            "fields":"[]"
        }
        kibana = Kibana(base_url=URL)
        res = kibana.object(space_id="demo", attribs=pattern_json).create('index-pattern')
        self.assertEqual(res.json()["attributes"], pattern_json)

    def test_import(self):
        pass
        file = open('data/example_no_subdata.ndjson', 'r')
        response = Kibana(base_url=URL).object().loads(file=file)
        file.close()
        print(response.json())

    def test_get_all_objects(self):
        pass
        response = Kibana(base_url=URL).object(space_id="demo").all(type="index-pattern")
        print(response.json())

    def test_create_panel(self):
        pass
        test = {'version': '7.8.0', 'gridData': {'x': 0, 'y': 12, 'w': 48, 'h': 12, 'i': 'holamundo'}, 'panelIndex': 'holamundo', 'embeddableConfig': {}, 'panelRefName': 'panel_0'}
        result = Panel("panel_0", 48, 12, 0, 12, id="holamundo", visualization_id="asdasdasd")
        print(result.get_reference())
        self.assertEqual(test, result.create())

    def test_create_visualization(self):
        pass
        pattern_json = {
            "title":"demo*",
            "timeFieldName": "@timestamp",
            "fields":"[]"
        }
        kibana = Kibana(base_url=URL)
        res = kibana.object(space_id="demo", attribs=pattern_json).create('index-pattern').json()
        index_pattern = res["id"]
        type = "histogram"
        title = "hello this is a visualization :D"
        visualization = Visualization(type=type, title=title, index_pattern_id=index_pattern).create()
        res = kibana.object(space_id="demo").create('visualization', body=visualization).json()
        print(res)

    def test_create_dashboard(self):
        pass
        pattern_json = {
            "title":"demo*",
            "timeFieldName": "@timestamp",
            "fields":"[]"
        }
        kibana = Kibana(base_url=URL)
        res = kibana.object(space_id="demo", attribs=pattern_json).create('index-pattern').json()
        index_pattern = res["id"]
        type = "histogram"
        title = "hello this is a visualization :D"
        visualization = Visualization(type=type, title=title, index_pattern_id=index_pattern).create()
        res = kibana.object(space_id="demo").create('visualization', body=visualization).json()
        visualization_id = res["id"]
        panel = Panel("panel_0", 48, 12, 0, 2, visualization_id=visualization_id)
        panels = [panel.create()]
        references = [panel.get_reference()]
        print(panels, references)
        dasboard = Dashboard(title="hola mundo", panels=panels, references=references, query="user.name: mat*").create()
        res = kibana.object(space_id="demo").create('dashboard', body=dasboard).json()
        print(res)


if __name__ == "__main__":
    unittest.main()