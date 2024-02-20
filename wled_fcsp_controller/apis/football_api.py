import requests


class FootballApi:
    def __init__(self, api_key: str):
        self.fcsp_id = "186"
        self.api_endpoint = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

    def get_current_match(self):
        querystring = {
            "live": "all",
            "team": self.fcsp_id
        }

        response = requests.get(self.api_endpoint, headers=self.headers, params=querystring)
        return response.json()

    def get_match_with_id(self, match_id: int):
        querystring = {
            "id": str(match_id)
        }

        response = requests.get(self.api_endpoint, headers=self.headers, params=querystring)
        return response.json()

    def get_next_match(self):
        querystring = {
            "team": self.fcsp_id,
            "next": "1"
        }

        response = requests.get(self.api_endpoint, headers=self.headers, params=querystring)
        return response.json()


if __name__ == '__main__':
    api = FootballApi('...')
    print(api.get_current_match().json())
