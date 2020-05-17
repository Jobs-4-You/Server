from elasticsearch.helpers import bulk
from elasticsearch_dsl import Index, Search

from elastic_db import Event, Job, es_session
from j4u_api.utils.data import get_clean_jobs_df


def seed_elastic():
    print("Seeding elastic ...")
    Job.init()
    j = get_clean_jobs_df().to_dict("records")
    ji = [
        Job(meta={"id": i}, **data).to_dict(include_meta=True)
        for i, data in enumerate(j)
    ]
    bulk(es_session, ji)
    Event.init()
    print("Elastic seeding done.")
