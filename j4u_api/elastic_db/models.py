from elasticsearch_dsl import Date, Document, Integer, Keyword, Object, Text


class Job(Document):
    avam = Integer()
    bfs = Integer()
    isco08 = Integer()
    title = Text(analyzer="snowball")
    isco_title = Text(analyzer="snowball")

    class Index:
        name = "jobs"
        settings = {
            "number_of_shards": 2,
        }


class Event(Document):
    timestamp = Date(default_timezone="UTC")
    user_agent = Text()
    ip = Keyword()
    type = Keyword()
    user_id = Keyword()
    payload = Object()

    class Index:
        name = "events"
        settings = {
            "number_of_shards": 2,
        }
