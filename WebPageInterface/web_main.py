from flask import Flask, render_template, json, url_for
from werkzeug.exceptions import HTTPException
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

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
    # print()
    # # validate if all manadatory data has been retrieved
    # # validateRetrievedData(data)
    # # SAF = SAF === none ? DEFAULT val : SAF;
    # # validated data object
    # # PASS the data to HTML
    #
    return render_template('login_page.html'), "Test page is working!"


@auth.login_required
@app.route("/rekuperatorius")
def _rekuperatorius():
    return render_template('rekup.html', title='REKUPERATORIUS')


@auth.login_required
@app.route("/durys")
def _duru_apsauga():
    return render_template('durys.html', title='APSAUGA')


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
