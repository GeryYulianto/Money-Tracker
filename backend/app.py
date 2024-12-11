from flask import Flask
from flask_app import FlaskApp
from features.login import LoginFeatures
from features.workspace import WorkSpaceFeatures
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

flask_app = Flask(__name__)
jwt = JWTManager()
jwt.init_app(flask_app)

app = FlaskApp(flask_app)
CORS(flask_app, resources={r"/*": {"origins": "*"}})
#Add features
login = LoginFeatures(flask_app)
login.add_endpoints()
workspace = WorkSpaceFeatures(flask_app)
workspace.add_workspace_endpoints()

if __name__ == "__main__":
    app.run(debug=True)