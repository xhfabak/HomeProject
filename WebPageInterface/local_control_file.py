import requests
import xmltodict
import datetime
import schedule
import xml.etree.ElementTree as ET


# ---- Set variables ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

# Rekuperatorius local connected IP address
_rekuperator_ip = 'http://192.168.0.200/'
_refresh_url = 'i.asp'
_send_request = 'ajax.xml'
_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
_xml_file = 'stored_rekup_data.xml'


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
def _handle_login_page():
    """Inject login  and password information to handle login page"""

    # TODO: make send this request once per hour (not constant refresh)
    # Login ('1') : Password ('2')
    login_data = {'1': 'user', '2': 'deltuvos31'}
    login_inject = requests.post(url=_rekuperator_ip, data=login_data)
    print(_current_time, '>> Login data was injected <<')


def _refresh_data(log_stamp: bool = False):
    """Komfovent page constantly sends updated information

    :param log_stamp: prints if this method is used (with timestamp)
    """

    # TODO: make refresh constant (make refresh every 5 seconds, not every )
    refreshed_data_ip = _rekuperator_ip + _refresh_url
    refreshed_data = requests.get(url=refreshed_data_ip)

    # Save 'ajax' response to file (XML)
    converted_response = ET.fromstring(refreshed_data.text)
    saved_data = ET.ElementTree(converted_response)
    saved_data.write(_xml_file)

    if log_stamp:
        print(_current_time, '>> Information was updated while trying to open page <<')


def _change_rekup_mode(mode):
    """Change ventilation system mode by using 'ajax.xml' inject """

    _current_rekuperatorius_mode_state(text='Mode before')  # Open saved (XML) file to print previous current state

    # Send request to change mode
    url = _rekuperator_ip + _send_request
    myobj = {'3': mode}  # '3' - mode request || mode - (int) of selected item
    request_to_change_mode = requests.post(url=url, data=myobj)

    _current_rekuperatorius_mode_state(text='Mode after')  # Return new changed state


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
def _income_temp_data() -> str:
    """Read XML file and return SUPPLY TEMPERATURE degrees

    :return: str of <AI0> xml file data
    """

    tree = ET.parse(_xml_file)
    root = tree.getroot()
    ai0_result = None
    for ai0 in root.findall('./AI0'):
        ai0_result = ai0.text

    return ai0_result


def _filter_data() -> str:
    """Read XML file and return FILTER percentage

    :return: str of <FCG> xml file data
    """

    tree = ET.parse(_xml_file)
    root = tree.getroot()
    fcg_result = None
    for fcg in root.findall('./FCG'):
        fcg_result = fcg.text

    return fcg_result


def _humidity_data() -> str:
    """Read XML file and return HUMIDITY percentage

    :return: str of <AH> xml file data
    """

    tree = ET.parse(_xml_file)
    root = tree.getroot()
    ah_result = None
    for ah in root.findall('./AH'):
        ah_result = ah.text

    return ah_result


def _current_rekuperatorius_mode_state(text: str) -> str:
    """Read XML file and return current rekuperatorius mode state

    :param text: print text
    :return: str of <OMO> xml file data
    """

    _refresh_data()

    tree = ET.parse(_xml_file)
    root = tree.getroot()
    omo_result = None
    for omo in root.findall('./OMO'):
        omo_result = omo.text

    print(_current_time, f'>> {text} - {omo_result}')  # add Previous mode name before changing.
    return omo_result

# schedule.every(1).hours.do(_handle_login_page)
# schedule.every(5).seconds.do(_refresh_data)
# schedule.run_pending()
# while True:
#     schedule.run_pending()