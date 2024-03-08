import time
import logging
logging.basicConfig()
logger = logging.getLogger('wled_control')
logger.setLevel(logging.DEBUG)

from datetime import datetime

import click

from wled_fcsp_controller.Score import Score
from wled_fcsp_controller.apis.spiegel_crawler import SpiegelCrawler
from wled_fcsp_controller.apis.wled_api import WLEDApi


@click.command()
@click.option('--ip_address', default='192.168.2.122', help='IP address of wled.')
def main(ip_address: str):

    wled_api = WLEDApi(ip_address)
    spiegel_crawler = SpiegelCrawler()
    logger.info(f'IP address: {ip_address}')

    current_score = Score(0, 0)
    while True:
        next_pauli_match_time = spiegel_crawler.next_pauli_match()
        if next_pauli_match_time is None:
            logger.info('no Pauli game in sight, sleep for 5 days')
            time.sleep(24 * 60 * 60 * 5)

        if next_pauli_match_time.date() != datetime.today().date() or (next_pauli_match_time > datetime.now() and (next_pauli_match_time - datetime.now()).total_seconds() > 1800):
            logger.info(f'Sleep until next Pauli match: {next_pauli_match_time}')
            time.sleep((next_pauli_match_time - datetime.now()).total_seconds())
            logger.info(f'Sleep is over, match starts: {next_pauli_match_time}')
            continue

        time.sleep(5)
        updated_score = spiegel_crawler.get_current_fcsp_score()
        logger.debug(f'Updated score: {updated_score}')
        if updated_score is None:
            current_score = Score(0, 0)
            time.sleep(90)
            continue

        if updated_score.fcsp > current_score.fcsp:
            logger.info(f'Pauli scored! New score: {updated_score}')
            wled_api.set_to_fcsp(30)
            time.sleep(1)

        if updated_score.other > current_score.other:
            logger.info(f'Pauli conceded a goal! New score: {updated_score}')
            wled_api.toggle_on_off(10)
            time.sleep(1)

        current_score = updated_score


if __name__ == '__main__':
    main()