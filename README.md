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