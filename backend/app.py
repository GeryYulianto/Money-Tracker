from flask import Flask
from flask_app import FlaskApp
from features.login import LoginFeatures

flask_app = Flask(__name__)

app = FlaskApp(flask_app)

#Add features
login = LoginFeatures()
login.add_ednpoint_login()

if __name__ == "__main__":
    app.run(debug=True)