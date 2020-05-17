import time

import pytest

import j4u_api.elastic_db
from j4u_api.app.app import app
from j4u_api.config import config
from j4u_api.gql.schema import schema
from j4u_api.qualtrics import qual_client
from j4u_api.utils.print import pretty_print
from j4u_api.utils.token import create_auth_token


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestEvents:
    def test_create_heartbeat(self, client):
        token = create_auth_token(1, 120)
        query = """
        mutation {
            createEvent(event:{
                type: "HEARTBEAT",
            }) {
                event {
                id
                payload
                }
            }
        }
        """
        a = client.post(
            "/graphql", json={"query": query}, headers={"accessToken": token}
        )
        print(a.json)
