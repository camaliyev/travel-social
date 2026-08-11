from flask import Flask
from extensions import db

app = Flask(__name__)

app.config["SECRET_KEY"] = "dev-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_social.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

from models import User, TravelPost
import routes

@app.route("/")
def home():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)