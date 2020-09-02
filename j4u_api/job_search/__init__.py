import pandas as pd
from fuzzywuzzy import fuzz, process

from j4u_api.config import config


class JobSearch:
    def __init__(self) -> None:
        df = pd.read_json(config.JOBS_JSON_PATH).rename(
            columns={
                "AVAM": "avam",
                "BFS": "bfs",
                "ISCO08": "isco08",
                "Title": "title",
                "ISCOTitle": "isco_title",
            }
        )
        df["id"] = df.index
        self.data = df.to_dict("index")
        self.data_search = {k: v["title"] for k, v in self.data.items()}

    def search(self, query, limit):
        matches = process.extract(
            query, self.data_search, limit=limit, scorer=fuzz.partial_token_sort_ratio
        )
        res = [self.data[i] for _, _, i in matches]
        return res


job_search_client = JobSearch()
