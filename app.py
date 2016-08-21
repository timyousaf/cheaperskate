import json
from flask import Flask, url_for, redirect, session, render_template, jsonify
from flask_oauth2_login import GoogleLogin
from plaid_client import PlaidClient

app = Flask(__name__)

app.config.update(
  SECRET_KEY="Miengous3Xie5meiyae6iu6mohsaiRae",
  GOOGLE_LOGIN_REDIRECT_SCHEME="http",
  GOOGLE_LOGIN_CLIENT_ID="209287169959-bbi3v6tpu99cb65ooos77c07gvmc7m4e.apps.googleusercontent.com",
  GOOGLE_LOGIN_CLIENT_SECRET="BTlujArOQlOc01RXeoIpFbML"
)

google_login = GoogleLogin(app)
finance_data = PlaidClient("/Users/timyousaf/plaid.txt")

@app.route("/charts")
def charts():
    print google_login.session()
    return render_template('charts.html')

@app.route("/test")
def test():
    return json.dumps(finance_data.getTransactions())

@app.route("/api/data")
def data():
    response = [
      {"name": 'Page A', "uv": 4000, "pv": 2400, "amt": 2400},
      {"name": 'Page B', "uv": 3000, "pv": 1398, "amt": 2210},
      {"name": 'Page C', "uv": 2000, "pv": 9800, "amt": 2290},
      {"name": 'Page D', "uv": 2780, "pv": 3908, "amt": 2000},
      {"name": 'Page E', "uv": 1890, "pv": 4800, "amt": 2181},
      {"name": 'Page F', "uv": 2390, "pv": 3800, "amt": 2500},
      {"name": 'Page G', "uv": 3490, "pv": 4300, "amt": 2100},
    ];
    return json.dumps(response)

@app.route("/")
def index():
  return """
<html>
<a href="{}">Login with Google</a>
""".format(google_login.authorization_url())

@google_login.login_success
def login_success(token, profile):
  return jsonify(token=token, profile=profile)

@google_login.login_failure
def login_failure(e):
  return jsonify(error=str(e))

app.run(debug=True)