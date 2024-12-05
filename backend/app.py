from flask import Flask
from flask_app import FlaskApp
from features.login import LoginFeatures
from features.workspace import WorkSpaceFeatures
from flask_cors import CORS

flask_app = Flask(__name__)

app = FlaskApp(flask_app)
CORS(flask_app, resources={r"/*": {"origins": "*"}})
#Add features
login = LoginFeatures(flask_app)
login.add_endpoint_login()
workspace = WorkSpaceFeatures(flask_app)
workspace.add_workspace_endpoints()

if __name__ == "__main__":
    app.run(debug=True)