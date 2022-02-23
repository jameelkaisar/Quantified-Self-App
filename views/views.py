import sys

sys.path.append("../models")
sys.path.append("../database")


from models.models import UserModel
from models.models import TrackerModel, TrackerTypes, TrackerUnit, TrackerOptions
from models.models import TrackerLogs, TrackerValues
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
from datetime import datetime


@app.route("/", methods=["GET"])
def home():
    return render_template("core/home.html", user=current_user)


@app.route("/trackers", methods=["GET"])
@login_required
def trackers():
    # trackers = TrackerModel.query.filter(TrackerModel.t_user == current_user.id).all()
    trackers = db.session.query(TrackerModel.t_id, TrackerModel.t_name, TrackerModel.t_desc).filter(TrackerModel.t_user == current_user.id).all()
    return render_template("trackers/main.html", user=current_user, trackers=trackers)


@app.route("/trackers/view", methods=["GET", "POST"])
@login_required
def trackers_view():
    t_id = request.args.get("id", "")
    if not (t_id.isdigit()):
        flash("Invalid Tracker", "danger")
        return redirect("/trackers")
    t_id = int(t_id)

    tracker = TrackerModel.query.filter(TrackerModel.t_id == t_id, TrackerModel.t_user == current_user.id).first()

    if not tracker:
        flash("Invalid Tracker", "danger")
        return redirect("/trackers")

    if request.method == "POST":
        action = request.form.get("action", "")
        if not (action.isdigit() and int(action) in [1, 2]):
            flash("Invalid Request", "danger")
            return redirect(request.full_path)
        action = int(action)

        if action == 1:
            db.session.delete(tracker)
            db.session.commit()
            flash("Tracker Deleted", "success")
            return redirect("/trackers")

        elif action == 2:
            flash("Log Creation Under Construction", "info")

            tl_time = request.form.get("tl_time", "")
            try:
                tl_time = datetime.strptime(tl_time, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Invalid Log Time", "danger")
                return redirect(request.full_path)

            tl_note = request.form.get("tl_note", "")
            if not (0 <= len(tl_note) <= 256):
                flash("Invalid Log Note", "danger")
                return redirect(request.full_path)

            tt_name = tracker.t_type_name.tt_name

            if tt_name in ["Boolean"]:
                flash("Boolean", "success")

                tl_val = request.form.get("tl_val", "")
                if tl_val == "1":
                    tl_val = 1
                elif tl_val == "0":
                    tl_val = 0
                else:
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)

                tl_vals = [tl_val]

            elif tt_name in ["Integer"]:
                flash("Integer", "success")

                tl_val = request.form.get("tl_val", "")
                try:
                    tl_val = int(float(tl_val))
                except ValueError:
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)

                tl_vals = [tl_val]

            elif tt_name in ["Decimal"]:
                flash("Decimal", "success")

                tl_val = request.form.get("tl_val", "")
                try:
                    tl_val = round(float(tl_val), 2)
                except ValueError:
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)

                tl_vals = [tl_val]

            elif tt_name in ["Duration"]:
                flash("Duration", "success")

                tl_val_h = request.form.get("tl_val_h", "")
                if not (tl_val_h.isdigit() and 0 <= int(tl_val_h) <= 100):
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)
                tl_val_h = int(tl_val_h)

                tl_val_m = request.form.get("tl_val_m", "")
                if not (tl_val_m.isdigit() and 0 <= int(tl_val_m) < 60):
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)
                tl_val_m = int(tl_val_m)

                tl_val_s = request.form.get("tl_val_s", "")
                if not (tl_val_s.isdigit() and 0 <= int(tl_val_s) < 60):
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)
                tl_val_s = int(tl_val_s)

                tl_val = (tl_val_h * 60 * 60) + (tl_val_m * 60) + (tl_val_s)
                tl_vals = [tl_val]

            elif tt_name in ["Single Select"]:
                flash("Single Select", "success")

                tl_val = request.form.get("tl_val", "")
                to_ids = list(map(lambda x: x.to_id, tracker.t_options))
                if not (tl_val.isdigit() and int(tl_val) in to_ids):
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)
                tl_val = int(tl_val)

                tl_vals = [tl_val]

            elif tt_name in ["Multi Select"]:
                flash("Multi Select", "success")

                tl_vals = []
                to_ids = list(map(lambda x: x.to_id, tracker.t_options))
                for i in to_ids:
                    tl_val = request.form.get(f"tl_val[{i}]", "")
                    if tl_val in ["1", "on"]:
                        tl_vals.append(i)
                if len(tl_vals) == 0:
                    flash("You must select at least one value", "info")
                    return redirect(request.full_path)

            log = TrackerLogs(tl_time=tl_time, tl_note=tl_note, tl_tracker=tracker.t_id)
            db.session.add(log)
            db.session.commit()
            for tl_val in tl_vals:
                val = TrackerValues(tv_val=tl_val, tv_log=log.tl_id)
                db.session.add(val)
            db.session.commit()
            flash("Log Added", "success")

            return redirect(request.full_path)

    options = {x.to_id: x.to_name for x in tracker.t_options}

    return render_template("trackers/view.html", user=current_user, tracker=tracker, options=options)


@app.route("/trackers/edit", methods=["GET", "POST"])
@login_required
def trackers_edit():
    t_id = request.args.get("id", "")
    if not (t_id.isdigit()):
        flash("Invalid Tracker", "danger")
        return redirect("/trackers")
    t_id = int(t_id)

    tracker = TrackerModel.query.filter(TrackerModel.t_id == t_id, TrackerModel.t_user == current_user.id).first()

    if not tracker:
        flash("Invalid Tracker", "danger")
        return redirect("/trackers")

    if request.method == "POST":
        t_name = request.form.get("t_name", "")
        if not (0 < len(t_name) <= 64):
            flash("Invalid Tracker Name", "danger")
            return redirect(request.full_path)

        t_desc = request.form.get("t_desc", "")
        if not (0 <= len(t_desc) <= 256):
            flash("Invalid Tracker Description", "danger")
            return redirect(request.full_path)

        tt_name = tracker.t_type_name.tt_name

        if tt_name in ["Boolean"]:
            flash("Boolean", "success")

            tracker.t_name = t_name
            tracker.t_desc = t_desc
            db.session.commit()
            flash("Tracker Edited", "success")

        elif tt_name in ["Integer", "Decimal"]:
            flash("Integer/Decimal", "success")

            t_unit = request.form.get("t_unit", "")
            if not (0 < len(t_unit) <= 16):
                flash("Invalid Tracker Unit", "danger")
                return redirect(request.full_path)
            flash("Unit", "success")

            tracker.t_name = t_name
            tracker.t_desc = t_desc
            db.session.commit()
            unit = TrackerUnit.query.filter(TrackerUnit.tu_tracker == t_id).one()
            unit.tu_name = t_unit
            db.session.commit()
            flash("Tracker Edited", "success")

        elif tt_name in ["Duration"]:
            flash("Duration", "success")

            tracker.t_name = t_name
            tracker.t_desc = t_desc
            db.session.commit()
            flash("Tracker Edited", "success")

        elif tt_name in ["Single Select", "Multi Select"]:
            flash("Single Select/Multi Select", "success")

            to_total = request.form.get("to_total", "")
            if not (to_total.isdigit() and int(to_total) > 0):
                flash("Invalid Tracker Options", "danger")
                return redirect(request.full_path)
            to_total = int(to_total)

            t_options = []
            for i in range(to_total):
                t_option = request.form.get(f"t_option[{i}]", "")
                if not (0 < len(t_option) <= 64):
                    flash("Invalid Tracker Options", "danger")
                    return redirect(request.full_path)
                t_options.append(t_option)
            flash("Options", "success")

            tracker.t_name = t_name
            tracker.t_desc = t_desc
            db.session.commit()

            to_count = 0

            for i in range(min(len(tracker.t_options), to_total)):
                option = tracker.t_options[i]
                option.to_name = t_options[i]
                to_count += 1

            for i in range(to_count, len(tracker.t_options)):
                # Handle Logs -> CASCADE?
                option = tracker.t_options[i]
                db.session.delete(option)
                to_count += 1

            for i in range(to_count, to_total):
                option = TrackerOptions(to_name=t_options[i], to_tracker=tracker.t_id)
                db.session.add(option)
                to_count += 1

            db.session.commit()
            flash("Tracker Edited", "success")

        return redirect(f"/trackers/view?id={t_id}")

    return render_template("trackers/edit.html", user=current_user, tracker=tracker)


@app.route("/trackers/add", methods=["GET", "POST"])
@login_required
def trackers_add():
    if request.method == "POST":
        t_name = request.form.get("t_name", "")
        if not (0 < len(t_name) <= 64):
            flash("Invalid Tracker Name", "danger")
            return redirect(request.full_path)

        t_desc = request.form.get("t_desc", "")
        if not (0 <= len(t_desc) <= 256):
            flash("Invalid Tracker Description", "danger")
            return redirect(request.full_path)

        t_type = request.form.get("t_type", "")
        tracker_types = TrackerTypes.query.all()
        if not (t_type.isdigit() and int(t_type) in map(lambda x: x.tt_id, tracker_types)):
            flash("Invalid Tracker Type", "danger")
            return redirect(request.full_path)
        t_type = int(t_type)

        tt_id = t_type
        tt_name = list(filter(lambda x: x.tt_id == tt_id, tracker_types))[0].tt_name

        if tt_name in ["Boolean"]:
            flash("Boolean", "success")

            tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=current_user.id)
            db.session.add(tracker)
            db.session.commit()
            flash("Tracker Added", "success")

        elif tt_name in ["Integer", "Decimal"]:
            flash("Integer/Decimal", "success")

            t_unit = request.form.get("t_unit", "")
            if not (0 < len(t_unit) <= 16):
                flash("Invalid Tracker Unit", "danger")
                return redirect(request.full_path)
            flash("Unit", "success")

            tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=current_user.id)
            db.session.add(tracker)
            db.session.commit()
            unit = TrackerUnit(tu_name=t_unit, tu_tracker=tracker.t_id)
            db.session.add(unit)
            db.session.commit()
            flash("Tracker Added", "success")

        elif tt_name in ["Duration"]:
            flash("Duration", "success")

            tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=current_user.id)
            db.session.add(tracker)
            db.session.commit()
            flash("Tracker Added", "success")

        elif tt_name in ["Single Select", "Multi Select"]:
            flash("Single Select/Multi Select", "success")

            to_total = request.form.get("to_total", "")
            if not (to_total.isdigit() and int(to_total) > 0):
                flash("Invalid Tracker Options", "danger")
                return redirect(request.full_path)
            to_total = int(to_total)

            t_options = []
            for i in range(to_total):
                t_option = request.form.get(f"t_option[{i}]", "")
                if not (0 < len(t_option) <= 64):
                    flash("Invalid Tracker Options", "danger")
                    return redirect(request.full_path)
                t_options.append(t_option)
            flash("Options", "success")

            tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=current_user.id)
            db.session.add(tracker)
            db.session.commit()
            for i in range(to_total):
                option = TrackerOptions(to_name=t_options[i], to_tracker=tracker.t_id)
                db.session.add(option)
            db.session.commit()
            flash("Tracker Added", "success")

        return redirect(f"/trackers/view?id={tracker.t_id}")

    tracker_types = TrackerTypes.query.all()
    return render_template("trackers/add.html", user=current_user, tracker_types=tracker_types)


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
