import threading
import time

from flask import Flask, render_template, json, url_for, request
from werkzeug.exceptions import HTTPException
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import local_control_file
from flask import jsonify
import datetime
import requests

app = Flask(__name__)
auth = HTTPBasicAuth()
# ---------------------------------------------------------------------------------------------------------------------

users = {
    "nologin": generate_password_hash("test123"),
    "safelogin": generate_password_hash("nopassword"),
    "admin": generate_password_hash("admin"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@auth.login_required
@app.route("/")
@app.route("/home")
def _home_main_page():
    return render_template('login_page.html'), "Test page is working!"


@auth.login_required
@app.route("/rekuperatorius")
def _main_rek_page():
    local_control_file.StoredDataFromFile.list_of_expected_data_to_return()
    return render_template('rekup.html', title='REKUPERATORIUS')


@auth.login_required
@app.route("/rekuperatorius/data")
def _return_data_from_json_file_to_web():
    """Return expected data from JSON file."""

    sorted_out = local_control_file.StoredDataFromFile.list_of_expected_data_to_return()

    return sorted_out


@auth.login_required
@app.route("/rekuperatorius", methods=["POST"])
def _change_ventilation_mode():
    """Send request to change mode."""

    mode_options = request.args.get("mode")
    local_control_file.GetData.change_device_ventilation_state(mode_options)  # Insert other number of Mode

    # TODO: fix, since need to return somekind of information
    return render_template('durys.html', title='APSAUGA')


@auth.login_required
@app.route("/durys")
def _door_lock():
    return render_template('durys.html', title='APSAUGA')


# ----- Constant refresh data -----------------------------------------------------------------------------------------
def run_login_every_hour():
    """Make constant login page information inject (otherwise refresh data will no be reached)."""
    while True:
        local_control_file.GetData.login_page_credentials_injection()
        time.sleep(60*45)  # minutes


def return_data_from_json_file_to_web():
    """Return expected data from JSON file to update data in webpage."""
    while True:
        local_control_file.StoredDataFromFile.list_of_expected_data_to_return()
        time.sleep(5)  # seconds


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    login_thread = threading.Thread(target=run_login_every_hour)
    login_thread.daemon = True
    login_thread.start()

    data_thread = threading.Thread(target=return_data_from_json_file_to_web)
    data_thread.daemon = True
    data_thread.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
