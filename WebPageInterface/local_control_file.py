import os

import requests
import xmltodict
import datetime
import schedule
import xml.etree.ElementTree as ET
import json


# ---- Set variables ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
# Rekuperatorius local connected IP address
_rekuperator_ip = 'http://192.168.0.200/'
_refresh_url = 'i.asp'
_send_request = 'ajax.xml'
_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
_xml_file = 'stored_rekup_data.xml'
_json_file = 'stored_rekup_data.json'


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
class GetData(object):
    """Main classes to get or send information."""

    @staticmethod
    def login_page_credentials_injection():
        """Inject login and password information to handle login page."""

        # Login ('1') : Password ('2')
        login_data = {'1': 'user', '2': 'deltuvos31'}
        requests.post(url=_rekuperator_ip, data=login_data)
        # TODO: add request check if POST was successful
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '>> Login data was injected <<')

    @staticmethod
    def refresh_data_from_device(log_stamp: bool = False):
        """Komfovent page constantly sends updated information

        :param log_stamp: prints if this method is used (with timestamp)
        """

        refreshed_data_ip = _rekuperator_ip + _refresh_url
        refreshed_data = requests.get(url=refreshed_data_ip)
        # TODO: add handling if GET was not successful

        GetData.save_requested_data_to_json(data=refreshed_data)

        if log_stamp:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  '>> Information was updated while trying to open page <<')

    @staticmethod
    def change_device_ventilation_state(mode):
        """Change ventilation system mode by using 'ajax.xml' inject """

        # Open saved (XML) file to print previous current state
        StoredDataFromFile.ventilation_program_state(text='Mode before')

        # Send request to change mode
        url = _rekuperator_ip + _send_request
        myobj = {'3': mode}  # '3' - mode request || mode - (int) of selected item
        request_to_change_mode = requests.post(url=url, data=myobj)
        # TODO: add handling if POST was not successful

        # Return new changed state
        StoredDataFromFile.ventilation_program_state(text='Mode after')

    @staticmethod
    def save_requested_data_to_json(data):
        """Helper method which saves XML response to JSON file.

        :param data: webpage 'i.asp' response with XML data
        """

        # Save 'ajax' response to file (XML)
        converted_response = ET.fromstring(data.text)
        saved_data = ET.ElementTree(converted_response)
        saved_data.write(_xml_file)
        # TODO: XML > JSON - Return JSON

        with open(_xml_file, 'r') as xml_data:
            convert = xmltodict.parse(xml_data.read())
            xml_data.close()
            json_data = json.dumps(convert)

            # write the json data to output
            with open(_json_file, "w") as json_file:
                json_file.write(json_data)
                json_file.close()


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
class StoredDataFromFile(object):
    """Get sorted information of """

    @staticmethod
    def income_temp_data() -> str:
        """Read XML file and return SUPPLY TEMPERATURE degrees

        :return: str of <AI0> xml file data
        """

        tree = ET.parse(_xml_file)
        root = tree.getroot()
        ai0_result = None
        for ai0 in root.findall('./AI0'):
            ai0_result = ai0.text

        return ai0_result

    @staticmethod
    def filter_data() -> str:
        """Read XML file and return FILTER percentage

        :return: str of <FCG> xml file data
        """

        tree = ET.parse(_xml_file)
        root = tree.getroot()
        fcg_result = None
        for fcg in root.findall('./FCG'):
            fcg_result = fcg.text

        return fcg_result

    @staticmethod
    def humidity_data() -> str:
        """Read XML file and return HUMIDITY percentage

        :return: str of <AH> xml file data
        """

        tree = ET.parse(_xml_file)
        root = tree.getroot()
        ah_result = None
        for ah in root.findall('./AH'):
            ah_result = ah.text

        return ah_result

    @staticmethod
    def ventilation_program_state(text: str) -> str:
        """Read XML file and return current rekuperatorius mode state

        :param text: print text
        :return: str of <OMO> xml file data
        """

        GetData.refresh_data_from_device()

        tree = ET.parse(_xml_file)
        root = tree.getroot()
        omo_result = None
        for omo in root.findall('./OMO'):
            omo_result = omo.text

        print(_current_time, f'>> {text} - {omo_result}')  # add Previous mode name before changing.
        return omo_result
