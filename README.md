# Kibana API Mapping Library

## Development Requirements
I only use `requests` to perform HTTP requests and pure logic for 
all behaviour.
## Installation

```bash
pip install kibana-api
```
## Usage and Examples

Configure Kibana Object:
```python
URL = "http://localhost:5601"
USERNAME = "XXXX"
PASSWORD = "XXXX"

```

### Create Space
```python
""
```
out:
```bash
""
```

### Create Object (index-pattern)
```python
""
```
out:
```bash
""
```

### Create Object (visualization)
```python
""
```
out:
```bash
""
```
### Create Object (dashboard)
```python
""
```
out:
```bash
""
```
### List all objects
```python
""
```
out:
```bash
""
```

## Development

Before starting you should run the `docker-compose.yml` file at `tests` folder (for 
testing purposes):

```yaml
version: '2.2'
services:
  es01:
    image: docker.elastic.co/elasticsearch/elasticsearch:${VERSION}
    container_name: es01
    environment:
      - node.name=es01
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es02,es03
      - cluster.initial_master_nodes=es01,es02,es03
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - data01:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
    networks:
      - elastic

  es02:
    image: docker.elastic.co/elasticsearch/elasticsearch:${VERSION}
    container_name: es02
    environment:
      - node.name=es02
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es01,es03
      - cluster.initial_master_nodes=es01,es02,es03
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - data02:/usr/share/elasticsearch/data
    networks:
      - elastic

  es03:
    image: docker.elastic.co/elasticsearch/elasticsearch:${VERSION}
    container_name: es03
    environment:
      - node.name=es03
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es01,es02
      - cluster.initial_master_nodes=es01,es02,es03
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - data03:/usr/share/elasticsearch/data
    networks:
      - elastic

  kib01:
    image: docker.elastic.co/kibana/kibana:${VERSION}
    container_name: kib01
    ports:
      - 5601:5601
    environment:
      ELASTICSEARCH_URL: http://es01:9200
      ELASTICSEARCH_HOSTS: '["http://es01:9200","http://es02:9200","http://es03:9200"]'
    networks:
      - elastic

volumes:
  data01:
    driver: local
  data02:
    driver: local
  data03:
    driver: local

networks:
  elastic:
    driver: bridge
```

Once the container is up you can validate every unit test:

```bash
python -m unittest tests.tests 
```

## Contributing
Yes fella, you know how ;)