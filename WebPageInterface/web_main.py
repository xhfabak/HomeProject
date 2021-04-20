import threading
import time

from flask import Flask, render_template, json, url_for, request
from werkzeug.exceptions import HTTPException
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import local_control_file
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


@app.route("/")
@app.route("/home")
@auth.login_required
def _home_main_page():
    return render_template('login_page.html'), "Test page is working!"


@auth.login_required
@app.route("/test")
def _testing():
    # TEST
    return render_template('login_page.html'), "Test page is working!"


@auth.login_required
@app.route("/rekuperatorius")
def _rekuperatorius():
    parsed_result = local_control_file.GetData.refresh_data_from_device(log_stamp=True)
    # TODO: Return parsedResult to HTML render_template method.
    return render_template('rekup.html', title='REKUPERATORIUS')


@app.route("/rekuperatorius", methods=["POST"])
def _change_ventilation_mode():
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
        time.sleep(60*60)  # sleep for 1 hour


def run_login_every_5sec():
    """Make constant data request from device to update data for page widgets."""
    while True:
        local_control_file.GetData.refresh_data_from_device()
        time.sleep(5)  # sleep for 5 seconds


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    login_thread = threading.Thread(target=run_login_every_hour)
    login_thread.daemon = True
    login_thread.start()

    data_thread = threading.Thread(target=run_login_every_5sec)
    data_thread.daemon = True
    data_thread.start()

    app.run(debug=True)
