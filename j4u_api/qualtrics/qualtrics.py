# curl -H 'X-API-TOKEN: yourapitoken' 'https://yourdatacenterid.qualtrics.com/API/v3/surveys'
import requests

from j4u_api.config import config


def pretty_print_req(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print(
        "{}\n{}\r\n{}\r\n\r\n{}".format(
            "-----------START-----------",
            req.method + " " + req.url,
            "\r\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
            req.body,
        )
    )


class Qualtrics:
    def __init__(self, token, data_center):
        self.token = token
        self.data_center = data_center

    @property
    def base_url(self):
        return f"https://{self.data_center}.qualtrics.com/API/v3"

    @property
    def headers(self):
        return {"X-API-TOKEN": self.token}

    def _make_request(self, mehtod, url):
        return requests.request(method=mehtod, url=url, headers=self.headers)

    def list_surveys(self):
        url = f"{self.base_url}/surveys"
        res = self._make_request("GET", url)
        data = res.json()["result"]["elements"]
        return data


qual_client = Qualtrics(config.QUALTRICS_TOKEN, "eu")
