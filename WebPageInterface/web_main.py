from flask import Flask, render_template, json, url_for, request
from werkzeug.exceptions import HTTPException
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import rekuperat
import schedule
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
    # GET XML data

    # # PARSE XML to JSON object
    # # CHECK how to parse XML > JSON
    # data = {}
    # # validate if all manadatory data has been retrieved
    # # validateRetrievedData(data)
    # # validated data object
    # # PASS the data to HTML
    return render_template('login_page.html'), "Test page is working!"


@auth.login_required
@app.route("/rekuperatorius")
def _rekuperatorius():

    schedule.every(1).hours.do(rekuperat._handle_login_page)  # TODO: fix with difference run
    schedule.every(5).seconds.do(rekuperat._refresh_data)  # TODO: fix with difference run
    schedule.run_pending()  # TODO: fix with difference run

    return render_template('rekup.html', title='REKUPERATORIUS')


@auth.login_required
@app.route("/durys")
def _duru_apsauga():
    return render_template('durys.html', title='APSAUGA')


@app.route("/rekuperatorius", methods=["POST"])
def _xuiznajit():
    rekup_mode = request.args.get("mode")
    print(rekup_mode)
    changeRekupMode(rekup_mode)  # Insert other number of Mode
    return render_template('durys.html', title='APSAUGA')  # TODO: fix, since need to return somekind of information


def changeRekupMode(mode):
    url = 'http://192.168.0.200/ajax.xml'
    myobj = {'3': mode}  # '3' - mode request || mode - (int) of selected item
    print('Hitted')  # add Previous mode name before changing.
    x = requests.post(url, data=myobj)
    print(x.status_code)  # add LOG after mode is changed, what new mode it is
    

# ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
