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

    local_control_file._handle_login_page()
    local_control_file._refresh_data(log_stamp=True)

    return render_template('rekup.html', title='REKUPERATORIUS')


@app.route("/rekuperatorius", methods=["POST"])
def _change_rekup_mode():
    mode_options = request.args.get("mode")
    local_control_file._change_rekup_mode(mode_options)  # Insert other number of Mode
    return render_template('durys.html', title='APSAUGA')  # TODO: fix, since need to return somekind of information


@auth.login_required
@app.route("/durys")
def _duru_apsauga():
    return render_template('durys.html', title='APSAUGA')


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
