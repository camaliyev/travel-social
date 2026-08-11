from flask import render_template, redirect, url_for, flash
from app import app
from extensions import db
from forms import RegistrationForm
from models import User


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = User.query.filter(User.username == form.username.data).first() or User.query.filter(User.email == form.email.data).first()
        if existing_user:
            flash("Username or email already exists. Please choose a different one.")
            return redirect(url_for("register"))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration succesful!")
        return redirect(url_for("home"))

    return render_template("register.html", form=form)
    