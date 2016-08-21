import json
from flask import Flask, url_for, redirect, session, render_template
from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)
from flask_googlelogin import GoogleLogin
from user import User

users = {}

app = Flask(__name__)
app.config.update(
    SECRET_KEY='Miengous3Xie5meiyae6iu6mohsaiRae',
    GOOGLE_LOGIN_CLIENT_ID='209287169959-bbi3v6tpu99cb65ooos77c07gvmc7m4e.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='BTlujArOQlOc01RXeoIpFbML',
    GOOGLE_LOGIN_REDIRECT_URI='http://localhost:5000/oauth2callback')
googlelogin = GoogleLogin(app)

@googlelogin.user_loader
def get_user(userid):
    return users.get(userid)

@app.route("/charts")
@login_required
def charts():
    return render_template('charts.html')

@app.route('/')
def index():
    return """
        <p><a href="%s">Login</p>
        <p><a href="%s">Login with extra params</p>
        <p><a href="%s">Login with extra scope</p>
    """ % (
        googlelogin.login_url(approval_prompt='force'),
        googlelogin.login_url(approval_prompt='force',
                              params=dict(extra='large-fries')),
        googlelogin.login_url(
            approval_prompt='force',
            scopes=['https://www.googleapis.com/auth/drive'],
            access_type='offline',
        ),
    )

@app.route('/profile')
@login_required
def profile():
    return """
        <p>Hello, %s</p>
        <p><img src="%s" width="100" height="100"></p>
        <p>Token: %r</p>
        <p>Extra: %r</p>
        <p><a href="/logout">Logout</a></p>
        """ % (current_user.name, current_user.picture, session.get('token'),
               session.get('extra'))

@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login(token, userinfo, **params):
    user = users[userinfo['id']] = User(userinfo)
    login_user(user)
    session['token'] = json.dumps(token)
    session['extra'] = params.get('extra')
    return redirect(params.get('next', url_for('.profile')))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return """
        <p>Logged out</p>
        <p><a href="/">Return to /</a></p>
        """

app.run(debug=True)