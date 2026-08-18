from flask import Flask, render_template, request
from extensions import db, login_manager, migrate
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel_social.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
migrate.init_app(app, db)

from models import User, TravelPost
import routes

@app.route("/")
def home():
    page = request.args.get("page", 1, type=int)

    posts = TravelPost.query.order_by(
        TravelPost.created_at.desc()
    ).paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    return render_template(
        "home.html",
        posts=posts
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

if __name__ == "__main__":
    app.run(debug=True)