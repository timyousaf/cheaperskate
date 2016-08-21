from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)

class User(UserMixin):
    def __init__(self, userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']
        self.picture = userinfo.get('picture')