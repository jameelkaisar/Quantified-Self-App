import sys

sys.path.append("../models")
sys.path.append("../database")


from models.models import UserModel, TrackerTypes
from database.database import db

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import flash
from flask import current_app as app
from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        t_name = request.form.get("t_name", None)
        t_desc = request.form.get("t_desc", None)
        t_type = request.form.get("t_type", None)
        to_total = request.form.get("to_total", None)

        print(t_name)
        print(t_desc)
        print(t_type)
        print(to_total)

        t_unit = request.form.get("t_unit", None)
        print(t_unit)

        t_options = []
        for i in range(int(to_total)):
            t_option = request.form.get(f"t_option[{i}]", None)
            t_options.append(t_option)
        print(t_options)

        flash("Some important message!", "primary")
        flash("Some important message!", "secondary")
        flash("Some important message!", "success")
        flash("Some important message!", "danger")
        flash("Some important message!", "warning")
        flash("Some important message!", "info")

        return redirect(request.full_path)

    tracker_types = TrackerTypes.query.all()
    return render_template("core/home.html", user=current_user, title="Home", tracker_types=tracker_types)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(request.args.get("next", "/"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(request.args.get("next", "/"))

    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", "")

        if UserModel.query.filter_by(username=username).first():
            return "Username Not Available"

        user = UserModel(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(request.args.get("next", "/"))

    return render_template("auth/register.html", request=request)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get("next", "/"))

    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", "")
        user = UserModel.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(request.args.get("next", "/"))
        else:
            return "Invalid Credentials"

    return render_template("auth/login.html", request=request)
