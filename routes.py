from flask import render_template, redirect, url_for, flash
from app import app
from extensions import db
from forms import RegistrationForm, LoginForm, TravelPostForm
from models import User, TravelPost
from flask_login import login_user, logout_user, login_required, current_user





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



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password. Please try again.")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("home"))

@app.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    form = TravelPostForm()

    if form.validate_on_submit():
        post = TravelPost(
            title=form.title.data,
            description=form.description.data,
            country=form.country.data,
            city=form.city.data,
            user_id=current_user.id 
        )

        db.session.add(post)
        db.session.commit()

        flash("Travel post created successfully!")
        return redirect(url_for("home"))

    return render_template("create_post.html", form=form)


@app.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts
    return render_template("profile.html", user=user, posts=posts)