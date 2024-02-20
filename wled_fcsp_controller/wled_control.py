import json
import time
import click
from pathlib import Path

from wled_fcsp_controller.Score import Score
from wled_fcsp_controller.apis.football_api import FootballApi
from wled_fcsp_controller.apis.wled_api import WLEDApi
from datetime import datetime

@click.command()
@click.option('--ip_address', default='192.168.2.123', help='IP address of wled.')
@click.option('--football_api_key', default='', help='API key for api-football-v1.p.rapidapi.com.')
def main(ip_address: str, football_api_key: str):
    debug = False
    football_api = FootballApi(football_api_key)
    wled_api = WLEDApi(ip_address)

    upcoming_game_id = None
    current_score = Score(0, 0)
    while True:
        if upcoming_game_id is not None or debug:
            match = football_api.get_match_with_id(upcoming_game_id) if not debug else get_example_game(True)
            assert len(match['response']) > 0

            match = match['response'][0]
            is_home_match = match['teams']['home']['name'] == 'FC St. Pauli'
            status = match['fixture']['status']['long']
            if status == 'Not Started':
                time.sleep(120)
            elif status == 'Match Finished':
                if match['teams']['home' if is_home_match else 'away']['winner']:
                    for i in range(5):
                        wled_api.set_to_fcsp(2)
                        time.sleep(2)
                    upcoming_game_id = None
                    current_score = Score(0, 0)
            else:
                updated_score = Score(match['goals']['home'], match['goals']['away']) if is_home_match else Score(match['goals']['away'], match['goals']['home'])

                if updated_score.fcsp > current_score.fcsp:
                    wled_api.set_to_fcsp(n_seconds=10)

                current_score = updated_score
                time.sleep(90)

        else:
            now = datetime.now()
            next_match = football_api.get_next_match() if not debug else get_example_game()
            match_datetime = datetime.fromtimestamp(next_match['response'][0]['fixture']['timestamp'])
            upcoming_game_id = next_match['response'][0]['fixture']['id']
            time.sleep((match_datetime - now).seconds + 60)


def get_example_game(modify: bool = False):
    with Path('wled_fcsp_controller/apis/example_repsonses/example_next_game.json').open('r') as f:
        result = json.load(f)
        if modify:
            result['response'][0]['fixture']['status']['long'] = 'Match Finished'
            result['response'][0]['goals']['away'] = 1
            result['response'][0]['teams']['away']['winner'] = True
        return result


if __name__ == '__main__':
    main()
