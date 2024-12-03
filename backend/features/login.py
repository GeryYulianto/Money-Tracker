from flask_app import FlaskApp
from flask import *

class LoginFeatures(FlaskApp):
    def login(self):
        if request.method == 'POST':
            pass
        else:
            pass

    def add_ednpoint_login(self):
        self.add_endpoint('/login', 'login', self.login, ['GET', 'POST'])