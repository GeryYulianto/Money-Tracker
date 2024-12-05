from flask_app import FlaskApp
from flask import *
from database.database import query_db

class LoginFeatures(FlaskApp):
    def __init__(self, app):
        super().__init__(app)
    def login(self):
        if request.method == 'POST':
            data = request.json
            username = data.get('username')
            password = data.get('password')
            user = query_db('''
                SELECT * FROM user
                WHERE username = ? AND password = ?
            ''', (username, password))
            if user:
                session['username'] = username
                return jsonify('Success'), 200
            else:
                return jsonify('Wrong'), 404

    def add_endpoint_login(self):
        self.add_endpoint('/login', 'login', self.login, ['GET', 'POST'])