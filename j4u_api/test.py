from datetime import datetime

from elasticsearch_dsl import Search

from j4u_api.elastic_db import Event, es_session

ev = Event(
    timestamp=int(datetime.now().timestamp()),
    ip="127.0.0.1",
    type="LOG",
    user_id=2,
    ajio=4,
)
ev.save()


s = Search(index="events").query("match_all")[:50]


response = s.execute()

print(dir(response))

print(len(response))

for hit in response:
    print(dir(hit))
