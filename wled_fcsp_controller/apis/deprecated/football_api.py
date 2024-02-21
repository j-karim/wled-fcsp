from typing import Dict

import click
import requests


class FootballApi:
    def __init__(self, api_key: str):
        self.fcsp_id = "186"
        self.rapid_api_endpoint = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        self.rapid_api_headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        self.sports_api_endpoint = "https://v3.football.api-sports.io/"
        self.sports_api_headers = {
            "x-apisports-key": api_key,
        }

        if self.connect(self.rapid_api_endpoint, self.rapid_api_headers):
            self.api_endpoint = self.rapid_api_endpoint
            self.api_headers = self.rapid_api_headers
        elif self.connect(self.sports_api_endpoint, self.sports_api_headers):
            self.api_endpoint = self.sports_api_endpoint
            self.api_headers = self.sports_api_headers
        else:
            raise ValueError('Given API key does not work for Football API')

    def connect(self, endpoint: str, headers: Dict):
        querystring = {
            "team": self.fcsp_id,
            "next": "1"
        }
        response = requests.get(endpoint, headers=headers, params=querystring)
        return response.status_code == 200

    def get_current_match(self):
        querystring = {
            "live": "all",
            "team": self.fcsp_id
        }

        response = requests.get(self.api_endpoint, headers=self.api_headers, params=querystring)
        return response.json()

    def get_match_with_id(self, match_id: int):
        querystring = {
            "id": str(match_id)
        }

        response = requests.get(self.api_endpoint, headers=self.api_headers, params=querystring)
        return response.json()

    def get_next_match(self):
        querystring = {
            "team": self.fcsp_id,
            "next": "1"
        }

        response = requests.get(self.api_endpoint, headers=self.api_headers, params=querystring)
        return response.json()


@click.command()
@click.option('--football_api_key', default='', help='API key for api-football-v1.p.rapidapi.com.')
def main(football_api_key: str):
    api = FootballApi(football_api_key)
    _ = api.get_next_match()


if __name__ == '__main__':
    main()
