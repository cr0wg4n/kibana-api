# Kibana API Mapping Library

Note: This unofficial library is only a proof of concept

[![Supported Versions](https://img.shields.io/pypi/pyversions/kibana-api.svg)](https://pypi.org/project/kibana-api/)
[![Downloads](https://pepy.tech/badge/kibana-api/month)](https://pepy.tech/project/kibana-api/month)


## Development Requirements
I only use `requests` to perform HTTP requests and pure logic for 
all behaviour.
## Installation
You can find this package in https://pypi.org/project/kibana-api/

```bash
pip install kibana-api
```
## Usage and Examples
If you going to test every example, you should run the `docker-compose.yml` example(development section).

Take a note: every `create` action returns a `<Requests>` Object as a result of HTTP request

### Configure Kibana Object:
```python
URL = "http://localhost:5601"
USERNAME = "XXXX" 
PASSWORD = "XXXX"
# username and password are optional fields
kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
```

### Create Space
```python
id = "demo"
name = "demo"
description = "descripcion del espacio de pruebas"
color = "#000000"
space = kibana.space(id=id, name=name, description=description, color=color)
space_response = space.create()
space_json = space_response.json()
```

### Create Object (index-pattern)
```python
pattern_json = {
    "title":"demo*",
    "timeFieldName": "@timestamp", #timefiledname is important, it taken as a reference to time
    "fields":"[]"
}
kibana = Kibana(base_url=URL, username=USERNAME, password=PASSWORD)
index_pattern_response = kibana.object(space_id="demo").create('index-pattern', attribs=pattern_json)
index_pattern_json = index_pattern.json()
```

### Create Object (visualization)
```python
type = "metric"
title = "Hello this is a basic metric visualization"
index_pattern_id = "XXXX-XXX-XXXX" # every visualization needs an index pattern to work
visualization = Visualization(type=type, title=title, index_pattern_id=index_pattern).create()
visualization_response = kibana.object(space_id="demo").create('visualization', body=visualization)
visualization_json = visualization_response.json()
```

### Visualization Modelation
```python
index_pattern = "XXXXX-XXXXXX-XXXXXX"
type = "line"
title = "Hello this is a basic line visualization"
visualization = Visualization(type=type, title=title, index_pattern_id=index_pattern)
visulization_model_json = visualization.create() # this operation returns a JSON body not a request response
```

### Panel Modelation
```python
width=48 
height=12
pos_x=0
pos_y=1
panel = Panel("panel_0", width, height, pos_x, pos_y, visualization_id=visualization_id)
panel_model_json = panel.create() # this operation returns a JSON body not a request response
references_model_json = panel.get_references() # this operation returns a JSON body not a request response
```

### Create Object (dashboard)
```python
index_pattern_id = "XXXXX-XXXXXX-XXXXXX"
type = "line"
title = "Hello this is a basic line visualization"
visualization = Visualization(type=type, title=title, index_pattern_id=index_pattern_id).create() # this operation returns a JSON body not a request response
visualization_response = kibana.object(space_id="demo").create('visualization', body=visualization)
visualization_json = visualization_response.json()
visualization_id = visualization_json["id"]

panel = Panel("panel_0", 48, 12, 0, 2, visualization_id=visualization_id)
panels = [panel.create()]
references = [panel.get_reference()]
dashboard = Dashboard(title="Demo Dashboard", panels=panels, references=references).create() # this operation returns a JSON body not a request response

dashboard_response = kibana.object(space_id=mock.space_id).create('dashboard', body=dashboard)
dashboard_json = dashboard_response.json()
```

### List all objects
```python
objects_response = kibana.object(space_id="demo").all() # All objects
objects_json = objects_response.json()
# Filter by types: "visualization", "dashboard", "search", "index-pattern", 
# "config", "timelion-sheet", "url", "query", "canvas-element", "canvas-workpad", "lens",
# "infrastructure-ui-source", "metrics-explorer-view", "inventory-view"
objects_response = kibana.object(space_id="demo").all(type="index-pattern") # Type in specific 
objects_json = objects_response.json()
```

### List all spaces
```python
spaces_response = kibana.space().all() # All spaces
spaces_json = spaces_response.json()
```

### Import Objects
```python
file = open("demo.ndjson", 'r')
response = kibana.object().loads(file=file)
file.close()
```

## Development

Before starting you should run the `docker-compose.yml` file at `tests` folder (for 
testing purposes):

```yaml
version: '2.2'

services:
  elastic:
    hostname: elasticsearch
    image: docker.elastic.co/elasticsearch/elasticsearch:${VERSION}
    container_name: elastic
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - discovery.type=single-node
      - xpack.security.enabled=true
      - xpack.security.audit.enabled=true
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - elastic_volume:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
    networks:
      - elastic

  kibana:
    image: docker.elastic.co/kibana/kibana:${VERSION}
    container_name: kibana
    ports:
      - 5601:5601
    environment:
      ELASTICSEARCH_URL: http://elasticsearch:9200
      ELASTICSEARCH_USERNAME: ${ELASTIC_USERNAME}
      ELASTICSEARCH_PASSWORD: ${ELASTIC_PASSWORD}
      ADMIN_PRIVILEGES: "true"
    networks:
      - elastic

volumes:
  elastic_volume:
    driver: local

networks:
  elastic:
    driver: bridge
```

The `.env` file cointains: 

```bash
VERSION=7.8.0
ELASTIC_USERNAME=elastic
ELASTIC_PASSWORD=elastic
```

Once the container is up you can validate every unit test:

```bash
python -m unittest tests.tests 
```

## Contributing
Yes fella, you know how ;)

## Contact Me

My blog: [cr0wg4n](https://cr0wg4n.medium.com/)

Twitter: [cr0wg4n](https://twitter.com/cr0wg4n)

Linkedin: [cr0wg4n](https://www.linkedin.com/in/cr0wg4n/)
