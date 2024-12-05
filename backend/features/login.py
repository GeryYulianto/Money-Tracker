from flask_app import FlaskApp
from flask import *
from flask_session import Session

class LoginFeatures(FlaskApp):
    def __init__(self, app):
        super().__init__(app)
    def login(self):
        if request.method == 'POST':
            request.form.get('username')
            
        else:
            pass

    def add_endpoint_login(self):
        self.add_endpoint('/login', 'login', self.login, ['GET', 'POST'])