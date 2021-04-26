import requests
import xmltodict
import datetime
import json
import time


# ---- Set variables ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
# Rekuperatorius local connected IP address
_rekuperator_ip = 'http://192.168.0.200/'
_refresh_url = 'i.asp'
_send_request = 'ajax.xml'
_current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
_json_file = 'server_response.json'


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
        refreshed_data = requests.get(url=refreshed_data_ip).text

        time.sleep(0.1)  # Magic delay

        GetData.save_requested_data_to_json(data=refreshed_data)

        if log_stamp:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '>> Information was updated while trying to open page <<')

    @staticmethod
    def read_json_data_from_file():
        """typo """

        with open(_json_file, "r") as json_file:
            result = json_file.read()

        return result

    @staticmethod
    def change_device_ventilation_state(mode):
        """Change ventilation system mode by using 'ajax.xml' to inject data to change mode."""

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
    def save_requested_data_to_json(data: str):
        """Helper method which saves XML response to JSON file.

        :param data: webpage 'i.asp' response with XML data
        """

        # Save 'i.asp' response (as string) as JSON
        convert = xmltodict.parse(data)
        json_data = json.dumps(convert)
        with open(_json_file, "w") as json_file:
            json_file.write(json_data)


# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
class StoredDataFromFile(object):
    """Get sorted information of """

    @staticmethod
    def check_expected_data_from_json(checking_data: str) -> str:
        """Read XML file and return degrees

        :param checking_data: check expected air ventilation system data element from JSON file to return result in page
        (AH - Humidity, FCG - Filter, AI0 - Supply temperature, VF -  Eco mode, EC4 - Heater power)
        :return: str of <AI0> xml file data
        """

        GetData.refresh_data_from_device()

        with open(_json_file, 'r') as read_file:
            json_data = json.load(read_file)
            returned_data = json_data['A'][checking_data]

            # Eco mode (VF) is returned as int (i.e "140656652")
            if checking_data == 'VF':
                rule = int(returned_data[:2])  # firs 2 numbers defines mode state
                if rule == 13:
                    returned_data = 'OFF'
                elif rule == 14:
                    returned_data = 'ON'
                else:
                    returned_data = 'Check mode result!'

            # Convert str response as int
            if checking_data == 'OMO':
                if returned_data == 'AWAY':
                    returned_data = 1
                elif returned_data == 'NORMAL':
                    returned_data = 2
                elif returned_data == 'INTENSE':
                    returned_data = 3
                elif returned_data == 'BOOST':
                    returned_data = 4

            return returned_data

    @staticmethod
    def ventilation_program_state(text: str) -> str:
        """Read XML file and return current rekuperatorius mode state

        :param text: text before returning result
        :return: str of <OMO> result
        """

        GetData.refresh_data_from_device()

        with open(_json_file, 'r') as read_file:
            json_data = json.load(read_file)
            omo_result = json_data['A']['OMO']

            print(_current_time, f'>> {text} - {omo_result}')  # add Previous mode name before changing.
            return omo_result

    @staticmethod
    def list_of_expected_data_to_return() -> dict:
        """Return expected data results to website to print constantly:
        Humidity / Income temperature (Supply) / Filter percentage / Eco mode (ON/OFF) / Heater power usage

        :return: returns dict of expected sorted items from JSON
        """

        curr_mode = StoredDataFromFile.check_expected_data_from_json('OMO')  # Current ventilation mode
        humidity = StoredDataFromFile.check_expected_data_from_json('AH')  # Humidity
        supply = StoredDataFromFile.check_expected_data_from_json('AI0')  # Supply temp
        filt = StoredDataFromFile.check_expected_data_from_json('FCG')  # Filter
        eco = StoredDataFromFile.check_expected_data_from_json('VF')  # Eco mode
        heater = StoredDataFromFile.check_expected_data_from_json('EC4')  # Heater power
        parsed_result = {
        "humidity": humidity,
        "supply": supply,
        "filter": filt,
        "eco": eco,
        "heater": heater,
        "curr_mode": curr_mode
        }

        return parsed_result


