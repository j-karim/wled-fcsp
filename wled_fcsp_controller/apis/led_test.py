import json
import time

import click

from wled_fcsp_controller.apis.wled_api import WLEDApi


@click.command()
@click.option('--ip_address', default='192.168.2.123', help='IP address of wled.')
def main(ip_address: str):
    request_helper = WLEDApi(ip_address)

    request_helper.set_to_fcsp(3)
    time.sleep(5)


if __name__ == '__main__':
    main()
