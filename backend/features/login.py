from flask import *
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import jsonpickle
from database.database import query_db

class LoginFeatures:
    def __init__(self, app):
        self.app = app

    def add_endpoints(self):
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                data = request.json
                username = data.get('username')
                password = data.get('password')
                user = query_db('''
                    SELECT * FROM user
                    WHERE username = ? AND password = ?
                ''', (username, password))
                if user:
                    access_token = create_access_token(identity=username)
                    return jsonify(access_token=access_token), 200
                else:
                    return jsonify('Wrong'), 404

        @self.app.route('/logout', methods=['GET'])
        @jwt_required()
        def logout():
            user = get_jwt_identity()
            return jsonpickle.encode(f'Logged out {user}'), 200