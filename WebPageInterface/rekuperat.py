import requests
import xmltodict
import json
import datetime
import time
from time import sleep
import schedule
from threading import Thread

# ---- Set variables ------------------------------------------------

# Rekuperatorius local connected IP address
_rekuperator_ip = 'http://192.168.0.200/'
refresh_url = 'i.asp'


def _handle_login_page():
    """Inject login  and password information to handle login page"""

    # TODO: make send this request once per hour (not constant refresh)

    # Login ('1') : Password ('2')
    login_data = {'1': 'user', '2': 'user'}
    last_run = datetime.datetime.today()
    login_inject = requests.post(url=_rekuperator_ip, data=login_data)
    print(last_run, '>> Login page was handled <<')


def _refresh_data():
    """Komfovent page constantly sends updated information"""

    # TODO: make refresh constant (make refresh every 5 seconds, not every )

    last_refresh = datetime.datetime.today()
    get_data = _rekuperator_ip + refresh_url
    refresh_data = requests.get(url=get_data)
    print(last_refresh, '>> Information was downloaded <<')


# schedule.every(5).seconds.do(_refresh_data)
# schedule.every(1).hours.do(_handle_login_page)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)