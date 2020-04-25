import json

import requests


class JobRoomClient:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            # "Postman-Token": "a22088d4-4d7f-4d72-b14d-bceb48ef23db",
            "X-Requested-With": "XMLHttpRequest",
            "cache-control": "no-cache",
        }
        self.search_url = (
            "https://www.job-room.ch/jobadservice/api/jobAdvertisements/_search"
        )

    def search(self, profession_codes, page):
        # params = (("page", int(data["currentPage"]) - 1), ("size", "10"), ("sort", "score"))
        params = {"page": page - 1, "size": 10, "sort": "score"}

        processed_codes = [{"type": "AVAM", "value": code} for code in profession_codes]

        data = {
            "permanent": None,
            "workloadPercentageMin": 0,
            "workloadPercentageMax": 100,
            "onlineSince": 30,
            "displayRestricted": False,
            "keywords": [],
            "professionCodes": processed_codes,
            "communalCodes": [],
            "cantonCodes": [],
        }

        response = requests.post(
            self.search_url, headers=self.headers, params=params, data=json.dumps(data)
        )
        total_count = response.headers.get("X-Total-Count", "0")
        positions = response.json()

        return total_count, positions
