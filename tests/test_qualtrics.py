from datetime import datetime

import pytest

from j4u_api.qualtrics import qual_client
from j4u_api.utils.print import pretty_print


class TestQualtricsDistributions:
    def test_create_distribution(self):
        surveys = qual_client.list_surveys()
        survey_id = surveys[0]["id"]

        mlist = qual_client.get_j4u_mailinglist()
        mlist_id = mlist["id"]

        qual_client.create_distribution(
            survey_id, mlist_id, datetime.now(), "Test distributions"
        )

        distribs = qual_client.list_distributions(survey_id)
        pretty_print(distribs)

        qual_client.delete_all_distributions(survey_id)

        distribs = qual_client.list_distributions(survey_id)
        pretty_print(distribs)

    def test_create_distribution_and_links(self):
        surveys = qual_client.list_surveys()
        survey_id = surveys[0]["id"]

        mlist = qual_client.get_j4u_mailinglist()
        mlist_id = mlist["id"]

        distrib, links = qual_client.create_distribution_and_links(
            survey_id, mlist_id, datetime.now(), "Test distributions"
        )
        pretty_print(links)

        distribs = qual_client.list_distributions(survey_id)
        pretty_print(distribs)

        qual_client.delete_all_distributions(survey_id)

        distribs = qual_client.list_distributions(survey_id)
        pretty_print(distribs)
