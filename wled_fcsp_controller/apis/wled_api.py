import json
import time
from copy import deepcopy
from typing import Dict

import requests


class WLEDApi:
    def __init__(self, ip_address: str):
        self.json_endpoint = f'http://{ip_address}/json'
        self.json_state_endpoint = f'http://{ip_address}/json/state'

    def get(self) -> Dict:
        """
        Get current led strip info
        :return: Dictionary containing state and info about led strip
        """
        return requests.get(self.json_endpoint).json()

    def post_state(self, state_dictionary: Dict) -> None:
        """
        Sets the led strip state with a state dictionary
        :param state_dictionary: new state
        """
        requests.post(self.json_state_endpoint, json.dumps(state_dictionary))

    def toggle_on_off(self, n_seconds: int) -> None:
        """
        Toggles the led strip
        """
        json_content = {"on": "t", "v": "true"}
        self.post_state(json_content)
        time.sleep(n_seconds)
        self.post_state(json_content)


    def set_to_fcsp(self, n_seconds: int = 10) -> None:
        """
        Sets the led strip to St Pauli colors (will be reset after n_seconds)
        :param n_seconds: Number of seconds to set the leds to Pauli colors
        """
        wled_dict = self.get()
        reset_status = deepcopy(wled_dict)
        n_leds = wled_dict['info']['leds']['count']

        fcsp_segments = [

            {
                "id": 0,
                "start": 0,
                "stop": int(n_leds / 3),
                "col": [
                    '624839',
                    '624839',
                    '624839',

                ],
                "bri": 255,
                "on": True,
            },
            {
                "id": 1,
                "start": int(n_leds / 3),
                "stop": int(2 / 3 * n_leds),
                "len": int(n_leds / 3),
                "col": [
                    'ffffff',
                    'ffffff',
                    'ffffff',
                ],
                "bri": 255,
                "on": True,
            },
            {
                "id": 2,
                "start": int(2 / 3 * n_leds),
                "stop": n_leds,
                "col": [
                    'e30613',
                    'e30613',
                    'e30613',
                ],
                "bri": 255,
                "on": True,
            }
        ]


        wled_dict['state']['seg'] = fcsp_segments
        wled_dict['state']['on'] = True

        self.post_state(wled_dict['state'])

        time.sleep(n_seconds)
        self.post_state(reset_status['state'])



