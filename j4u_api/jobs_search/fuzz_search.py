from fuzzywuzzy import process

from j4u_api.utils.data import prepare_jobs


class JobsFuzzSearch:
    def __init__(self):
        records, choices_dict = prepare_jobs()
        self.records = records
        self.choices_dict = choices_dict

    def search(self, query, limit):
        matches = process.extract(query, self.choices_dict, limit=limit)
        print(matches)
        results = []
        for _, _, i in matches:
            res = dict(self.records[i])
            res["id"] = i
            results.append(res)
        return results
