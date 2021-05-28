import time
import json
from kibana_api import Dashboard, Panel, Visualization, Kibana, kibana
import random
import unittest
import os

URL = "http://localhost:5601"
ELASTIC_DEMO_INDEX_URL = "http://localhost:9200/index_demo/_doc"
USERNAME = "elastic"
PASSWORD = "elastic"


class mock:
    index_pattern_id = ""
    space_id = ""
    visualization_id = ""

class TestStringMethods(unittest.TestCase):

    def test_ping(self):
        # return True
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        test = True
        ping = kibana.ping() # True or False
        self.assertEqual(ping, test)

    def test_url_parser(self):
        # return True
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        url = kibana.url(URL, "1", "2", "3")
        self.assertEqual("http://localhost:5601/1/2/3", url)

    def test_generate_data(self):
        # return True
        data = {
           "@timestamp": "2021-05-26T13:40:15.000Z",
            "user": {
                "name": "matias max",
                "email": "mcm.12@asd.com",
                "age": 22
            }
        }
        response = Kibana(base_url=URL, username=USERNAME, password=PASSWORD).requester(url=ELASTIC_DEMO_INDEX_URL, method="post", data=json.dumps(data))
        print("generated data:", response)
        self.assertEqual(201, response.status_code)


    def test1_create_space(self):
        # return True
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        id = "test-{}".format(int(random.randint(0,100)*0.33))
        name = id
        description = "space description"
        color = "#000000"
        response = kibana.space(id=id, name=name, description=description, color=color).create()
        response_json = {
            "id": id,
            "name": name,
            "description": description,
            "color": color,
            "disabledFeatures": []
        }
        mock.space_id = id
        print("space created: ", mock.space_id)
        self.assertEqual(response.json(), response_json)

    def test2_create_index_pattern(self):
        # return True
        pattern_json = {
            "title":"index*",
            "timeFieldName": "@timestamp",
            "fields":"[]"
        }
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        response = kibana.object(space_id=mock.space_id).create('index-pattern', attribs=pattern_json).json()
        mock.index_pattern_id = response["id"]
        print("index created: ", mock.index_pattern_id)
        self.assertEqual(response["attributes"], pattern_json)

    def test3_import(self):
        # return True
        CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        FILE_PATH = os.path.join(CURRENT_DIR, 'exported_data.ndjson')

        file = open(FILE_PATH, 'r')
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        response = kibana.object(space_id=mock.space_id).loads(file=file)
        file.close()
        print(response)

    def test4_get_all_objects(self):
        # return True
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        response = kibana.object(space_id=mock.space_id).all(type="index-pattern")
        print(response)

    def test5_create_panel(self):
        # return True
        panel_id = "XXXXX"
        test = {'version': '7.8.0', 'gridData': {'x': 0, 'y': 12, 'w': 48, 'h': 12, 'i': panel_id}, 'panelIndex': panel_id, 'embeddableConfig': {}, 'panelRefName': 'panel_0'}
        result = Panel("panel_0", 48, 12, 0, 12, id=panel_id)
        self.assertEqual(test, result.create())

    def test6_create_visualization(self):
        # return True
        type = "line"
        title = "hello this is a visualization :D 2"
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        visualization_obj = Visualization(type=type, title=title, index_pattern_id=mock.index_pattern_id).create()
        response = kibana.object(space_id=mock.space_id).create('visualization', body=visualization_obj).json()
        mock.visualization_id = response["id"]
        print("visualization created: ", mock.visualization_id)

    def test7_create_dashboard(self):
        # return True
        panel = Panel("panel_0", 48, 12, 0, 2, visualization_id=mock.visualization_id)
        panels = [panel.create()]
        references = [panel.get_reference()]
        dashboard = Dashboard(title="hola mundo", panels=panels, references=references, query="user.name: mat*").create()
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        response = kibana.object(space_id=mock.space_id).create('dashboard', body=dashboard).json()
        dashboard_id = response["id"]
        print("dashboard created: ", dashboard_id)

    def test8_object_by_id(self):
        # return True
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        reponse = kibana.object(space_id=mock.space_id).get(id=mock.visualization_id, type="visualization")
        print(reponse)

    def test9_get_all_spaces(self):
        kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
        response = kibana.space().all().json()
        print(response)

if __name__ == "__main__":
    unittest.main()