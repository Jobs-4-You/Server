from config import config
from elastic import es
from elastic.elastic import es, delete_all_indices, create_indexes, import_jobs
from datetime import datetime

#delete_all_indices()
#create_indexes()
#import_jobs()
##delete_all_indices()

es.indices.refresh(index="jobs-index")
a = es.count(index="jobs-index")
res = es.search(
    index="jobs-index", body={"query": {"wildcard": {"title": {"value": "caiss*"}}}}
)
print(res)

