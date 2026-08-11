from flask import Flask, render_template
from extensions import db, login_manager

app = Flask(__name__)

app.config["SECRET_KEY"] = "dev-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_social.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

from models import User, TravelPost
import routes

@app.route("/")
def home():
    posts = TravelPost.query.order_by(TravelPost.created_at.desc()).all()

    return render_template("home.html", posts=posts)


if __name__ == "__main__":
    app.run(debug=True)