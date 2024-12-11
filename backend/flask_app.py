from flask import *
from flask_session import Session
from database.database import query_db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

load_dotenv()
class FlaskApp():
    def __init__(self, app):
        self.app = app
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        self.app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
        self.app.config['JWT_TOKEN_LOCATION'] = ['headers']
        self.jwt = JWTManager()

    def add_endpoint(self, endpoint, endpoint_name, handler, methods):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods)
    
    def run(self):
        self.app.run(debug=True)