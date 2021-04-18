import requests
import xmltodict
import datetime
import schedule
import xml.etree.ElementTree as ET


# ---- Set variables ------------------------------------------------

# Rekuperatorius local connected IP address
_rekuperator_ip = 'http://192.168.0.200/'
refresh_url = 'i.asp'
send_request = 'ajax.xml'
current_time = datetime.datetime.today()


def _handle_login_page():
    """Inject login  and password information to handle login page"""

    # TODO: make send this request once per hour (not constant refresh)

    # Login ('1') : Password ('2')
    login_data = {'1': 'user', '2': 'user'}
    login_inject = requests.post(url=_rekuperator_ip, data=login_data)
    print(current_time, '>> Login page was handled <<')


def _refresh_data():
    """Komfovent page constantly sends updated information"""

    # TODO: make refresh constant (make refresh every 5 seconds, not every )

    get_data = _rekuperator_ip + refresh_url
    refresh_data = requests.get(url=get_data)

    # Save ajax response (XML) to file
    converted_response = ET.fromstring(refresh_data.text)
    saved_data = ET.ElementTree(converted_response)
    saved_data.write("refreshed_data.xml")
    print(current_time, '>> Information was updated <<')


def _change_rekup_mode(mode):
    """Change ventilation system mode by using 'ajax.xml' inject """

    url = _rekuperator_ip + send_request
    print(current_time, 'Previous <><><> mode')  # add Previous mode name before changing.
    myobj = {'3': mode}  # '3' - mode request || mode - (int) of selected item
    x = requests.post(url, data=myobj)
    print(current_time, x.status_code)  # add LOG after mode is changed, what new mode it is

# schedule.every(1).hours.do(_handle_login_page)
# schedule.every(5).seconds.do(_refresh_data)
# schedule.run_pending()
# while True:
#     schedule.run_pending()