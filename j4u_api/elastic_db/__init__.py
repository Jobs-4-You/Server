from elasticsearch_dsl import connections

from j4u_api.config import config

from .models import Event, Job

# Define a default Elasticsearch client
es_session = connections.create_connection(hosts=[config.ELASTIC_URL])
