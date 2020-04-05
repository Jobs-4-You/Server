import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from config import config

from .mappings import job_mapping

es = Elasticsearch(
    ["localhost"], http_auth=(config.ELASTIC_USER, config.ELASTIC_PW), maxsize=25
)


def create_all_indices():
    print("Start creating elasticsearch indices ...")
    es.indices.create(index="jobs-index", body=job_mapping)
    print("Done.")


def delete_all_indices():
    print("Start deleting elasticsearch indices ...")
    indices = es.indices.get_alias("*").keys()
    for index in indices:
        es.indices.delete(index)
    print("Done.")


def process_job(job):
    job = {
        "avam": job["AVAM"],
        "bfs": job["BFS"],
        "isco08": job["ISCO08"],
        "title": job["Title"],
        "isco_title": job["ISCOTitle"],
    }
    _id = job["avam"]
    return _id, job


def import_jobs():
    print("Start importing jobs ...")
    with open("storage/jobs.json", "r") as f:
        jobs = json.load(f)

    data = []
    for job in jobs:
        _id, job = process_job(job)
        data.append(
            {"_index": "jobs-index", "_type": "_doc", "_id": _id, "_source": job}
        )
    bulk(es, data)
    print("Done.")
