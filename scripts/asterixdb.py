import json
import logging

import requests


class AsterixDB:
    def __init__(self, server_uri, dataverse):
        self.server_uri = server_uri
        self.dataverse = dataverse

    def run(self, query):
        query_uri = 'http://{server_uri}/query/service'.format(
            server_uri=self.server_uri)
        logging.info('Running query against %s', query_uri)

        response = requests.post(query_uri, {'statement': query})

        return json.loads(response.text)
