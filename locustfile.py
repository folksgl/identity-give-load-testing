""" Locustfile for load testing GIVE functionality """
import time
import os
import random
from locust import HttpUser, task, constant

CLIENT_SECRET = str(os.environ["CLIENT_SECRET"])
CLIENT_ID = str(os.environ["CLIENT_ID"])


class GiveUser(HttpUser):
    wait_time = constant(1)
    bearer_token = None

    @task
    def idemia_locations(self):
        """ Perform GET on the idemia /locations endpoint """
        zipcode = random.randrange(10000, 99999)
        self.client.get(
            "/ipp/locations/%i" % zipcode,
            name="/locations/zipcode",
            headers={"Authorization": self.bearer_token},
        )

    def on_start(self):
        """ Generate the OAuth2.0 token for the user """
        response = self.client.post(
            "/ipp/oauth2/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "client_credentials",
                "scope": "rpname",
            },
        )
        json_response = response.json()
        self.bearer_token = f"token {json_response['access_token']}"
