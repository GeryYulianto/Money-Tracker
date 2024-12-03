from flask import Flask
from flask_app import FlaskApp

flask_app = Flask(__name__)

app = FlaskApp(flask_app)

#Add features

if __name__ == "__main__":
    app.run(debug=True)