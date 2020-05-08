import requests

from j4u_api.config import config

from .export import export


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

    def _make_request(self, mehtod, url, json=None, params=None):
        if json is not None and mehtod == "GET":
            raise Exception("Cannot use method GET with json argument")
        if params is not None and mehtod == "POST":
            raise Exception("Cannot use method POST with params argument")

        if json is not None and mehtod == "POST":
            return requests.request(
                method=mehtod, url=url, headers=self.headers, json=json
            )
        if params is not None and mehtod == "GET":
            return requests.request(
                method=mehtod, url=url, headers=self.headers, params=params
            )

        return requests.request(method=mehtod, url=url, headers=self.headers)

    # Surveys related
    def list_surveys(self):
        url = f"{self.base_url}/surveys"
        res = self._make_request("GET", url)
        data = res.json()["result"]["elements"]
        return data

    def list_libraries(self):
        url = f"{self.base_url}/libraries"
        res = self._make_request("GET", url)
        data = res.json()["result"]["elements"]
        return data

    def list_library_surveys(self, library_id):
        url = f"{self.base_url}/libraries/{library_id}/survey/surveys"
        res = self._make_request("GET", url)
        data = res.json()["result"]["elements"]
        return data

    # Exports related
    def export_responses(self, survey_id):
        return export(self.token, self.data_center, survey_id)

    # Contacts related
    def list_mailinglists(self):
        url = f"{self.base_url}/mailinglists"
        res = self._make_request("GET", url)
        data = res.json()["result"]["elements"]
        return data

    def get_mailinglist(self, mailinglist_id):
        url = f"{self.base_url}/mailinglists/{mailinglist_id}"
        res = self._make_request("GET", url)
        data = res.json()["result"]
        return data

    def get_contacts(self, mailinglist_id):
        url = f"{self.base_url}/mailinglists/{mailinglist_id}/contacts"
        res = self._make_request("GET", url)
        data = res.json()["result"]["elements"]
        return data

    def get_j4u_mailinglist(self):
        mlists = self.list_mailinglists()
        mlists = [m for m in mlists if "J4U-PLATFORM" in m["name"]]
        if len(mlists) > 1:
            raise Exception("Duplicated mailing list")
        elif len(mlists) == 0:
            raise Exception("Mailing list not found")
        return mlists[0]

    def get_j4u_contacts(self):
        mlist = self.get_j4u_mailinglist()
        contacts = self.get_contacts(mlist["id"])
        return contacts

    def create_contact(self, email):
        mlist = self.get_j4u_mailinglist()

        contacts = self.get_j4u_contacts()
        print(contacts)
        exists = email in [x["email"] for x in contacts]

        if exists:
            raise Exception(f"Contact with email: {email} already exists")

        mlist_id = mlist["id"]
        url = f"{self.base_url}/mailinglists/{mlist_id}/contacts"
        res = self._make_request("POST", url, json={"email": email})

    # Distribution related
    def list_distributions(self, survey_id):
        url = f"{self.base_url}/distributions"
        res = self._make_request("GET", url, params={"surveyId": survey_id})
        data = res.json()["result"]["elements"]
        return data

    def get_distribution(self, distribution_id, survey_id):
        url = f"{self.base_url}/distributions/{distribution_id}"
        res = self._make_request("GET", url, params={"surveyId": survey_id})
        data = res.json()["result"]["elements"]
        return data

    def delete_distribution(self, distribution_id):
        url = f"{self.base_url}/distributions/{distribution_id}"
        res = self._make_request("DELETE", url)
        data = res.json()
        print(data, "aaaaaaaaa")
        return data

    def delete_all_distributions(self, survey_id):
        distributions = self.list_distributions(survey_id)
        for distrib in distributions:
            self.delete_distribution(distrib["id"])
        print(f"{len(distributions)} distributions deleted")

    def create_distribution(self, survey_id, mlist_id, expiration_dt, desc):
        url = f"{self.base_url}/distributions"
        data = {
            "surveyId": survey_id,
            "linkType": "Individual",
            "description": desc,
            "action": "CreateDistribution",
            "expirationDate": expiration_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "mailingListId": mlist_id,
        }
        res = self._make_request("POST", url, json=data)
        data = res.json()["result"]
        return data

    def get_distribution_links(self, distrib_id, survey_id):
        url = f"{self.base_url}/distributions/{distrib_id}/links"
        res = self._make_request("GET", url, params={"surveyId": survey_id})
        data = res.json()["result"]["elements"]
        return data

    def create_distribution_and_links(self, survey_id, *args):
        distrib = self.create_distribution(survey_id, *args)
        links = self.get_distribution_links(distrib["id"], survey_id)
        return distrib, links


qual_client = Qualtrics(config.QUALTRICS_TOKEN, "eu")
