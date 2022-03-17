import sys

sys.path.append("../models")
sys.path.append("../database")


from models.models import UserModel
from models.models import TrackerModel, TrackerTypes, TrackerUnit, TrackerOptions
from models.models import TrackerLogs, TrackerValues
from models.models import APIToken
from database.database import db

from flask import request
from flask import redirect
from flask import render_template
from flask import flash
from flask import url_for
from flask import current_app as app
from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from sqlalchemy import desc, nullsfirst
from datetime import datetime

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from pathlib import Path
import csv
import os


@app.route("/", methods=["GET"])
def home():
    # return render_template("core/home.html", user=current_user)

    if current_user.is_authenticated:
        return redirect("/trackers")
    else:
        return redirect("/login")


@app.route("/api/v1", methods=["GET"])
def api_v1():
    return render_template("api/api_v1.html", user=current_user)


@app.route("/api", methods=["GET", "POST"])
@login_required
def api():
    if request.method == "POST":
        action = request.form.get("action", "")
        if not (action.isdigit() and int(action) in [1]):
            flash("Invalid Request", "danger")
            return redirect(request.full_path)
        action = int(action)

        if action == 1:
            tokens = APIToken.query.all()
            tokens = list(map(lambda x: x.api_token, tokens))
            token = os.urandom(32).hex()
            while token in tokens:
                token = os.urandom(32).hex()
            api_token = APIToken.query.filter(APIToken.api_user == current_user.id).first()
            api_token.api_token = token
            db.session.commit()

        return redirect("/api")

    return render_template("api/api.html", user=current_user)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    trackers = TrackerModel.query.filter(TrackerModel.t_user == current_user.id).all()

    export_options = {1: "CSV", 2: "TSV"}

    if request.method == "POST":
        action = request.form.get("action", "")
        if not (action.isdigit() and int(action) in [1]):
            flash("Invalid Request", "danger")
            return redirect(request.full_path)
        action = int(action)

        if action == 1:
            e_format = request.form.get("e_format", "")
            if not (e_format.isdigit() and int(e_format) in export_options):
                flash("Invalid Request", "danger")
                return redirect(request.full_path)
            e_format = int(e_format)

            Path(f"static/userdata/dashboard/logs/{current_user.id}/").mkdir(parents=True, exist_ok=True)

            now = datetime.now()
            now_str = now.strftime("%Y%m%d_%H%M%S_%f")

            if e_format == 1:
                count = 0
                with open(f"static/userdata/dashboard/logs/{current_user.id}/quantified_self_app_logs_{now_str}.csv", "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["S No", "Tracker ID", "Tracker Name", "Tracker Description", "Tracker Type ID", "Tracker Type Name", "Tracker Unit", "Log ID", "Log Time", "Log Note", "Log Value"])
                    for tracker in trackers:
                        t_id = tracker.t_id
                        t_name = tracker.t_name
                        t_desc = tracker.t_desc
                        t_type = tracker.t_type
                        tt_name = tracker.t_type_name.tt_name
                        if tt_name in ["Integer", "Decimal"]:
                            tu_name = tracker.t_unit.tu_name
                        else:
                            tu_name = None
                        t_logs = tracker.t_logs
                        for log in t_logs:
                            tl_id = log.tl_id
                            tl_time = log.tl_time
                            tl_note = log.tl_note
                            tl_vals = log.tl_vals
                            for tl_val in tl_vals:
                                tv_val = tl_val.tv_val
                                count += 1
                                writer.writerow([count, t_id, t_name, t_desc, t_type, tt_name, tu_name, tl_id, tl_time, tl_note, tv_val])

                return redirect(url_for("static", filename=f"userdata/dashboard/logs/{current_user.id}/quantified_self_app_logs_{now_str}.csv"))

            elif e_format == 2:
                count = 0
                with open(f"static/userdata/dashboard/logs/{current_user.id}/quantified_self_app_logs_{now_str}.tsv", "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                    writer.writerow(["S No", "Tracker ID", "Tracker Name", "Tracker Description", "Tracker Type ID", "Tracker Type Name", "Tracker Unit", "Log ID", "Log Time", "Log Note", "Log Value"])
                    for tracker in trackers:
                        t_id = tracker.t_id
                        t_name = tracker.t_name
                        t_name = t_name.replace("\t", "    ")
                        t_name = t_name.replace("\n", "    ")
                        t_name = t_name.replace("\r", "")
                        t_desc = tracker.t_desc
                        t_desc = t_desc.replace("\t", "    ")
                        t_desc = t_desc.replace("\n", "    ")
                        t_desc = t_desc.replace("\r", "")
                        t_type = tracker.t_type
                        tt_name = tracker.t_type_name.tt_name
                        tt_name = tt_name.replace("\t", "    ")
                        tt_name = tt_name.replace("\n", "    ")
                        tt_name = tt_name.replace("\r", "")
                        if tt_name in ["Integer", "Decimal"]:
                            tu_name = tracker.t_unit.tu_name
                            tu_name = tu_name.replace("\t", "    ")
                            tu_name = tu_name.replace("\n", "    ")
                            tu_name = tu_name.replace("\r", "")
                        else:
                            tu_name = None
                        t_logs = tracker.t_logs
                        for log in t_logs:
                            tl_id = log.tl_id
                            tl_time = log.tl_time
                            tl_note = log.tl_note
                            tl_note = tl_note.replace("\t", "    ")
                            tl_note = tl_note.replace("\n", "    ")
                            tl_note = tl_note.replace("\r", "")
                            tl_vals = log.tl_vals
                            for tl_val in tl_vals:
                                tv_val = tl_val.tv_val
                                count += 1
                                writer.writerow([count, t_id, t_name, t_desc, t_type, tt_name, tu_name, tl_id, tl_time, tl_note, tv_val])

                return redirect(url_for("static", filename=f"userdata/dashboard/logs/{current_user.id}/quantified_self_app_logs_{now_str}.tsv"))

    Path(f"static/userdata/dashboard/graphs/{current_user.id}/").mkdir(parents=True, exist_ok=True)

    for tracker in trackers:
        try:
            if tracker.t_type_name.tt_name in ["Boolean"]:
                logs = tracker.t_logs

                if len(logs) < 1:
                    plt.annotate('Add more logs to see the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                    plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
                    plt.clf()
                    continue

                x = ["Yes", "No"]
                y = [sum(map(lambda x: int(x.tl_vals[0].tv_val), logs))]
                y.append(len(logs) - y[0])

                patches, texts, _ = plt.pie(y, autopct='%1.0f%%')
                plt.legend(patches, x, loc='upper right', bbox_to_anchor=(1.2, 1.))

                plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
                plt.clf()

            elif tracker.t_type_name.tt_name in ["Integer", "Decimal"]:
                logs = tracker.t_logs

                if len(logs) < 3:
                    plt.annotate('Add more logs to see the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                    plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
                    plt.clf()
                    continue

                x, y = zip(*map(lambda x: (x.tl_time, int(x.tl_vals[0].tv_val)), logs))

                x_0 = int(x[0].strftime('%Y%m%d%H%M%S%f'))
                xint = [(int(d.strftime('%Y%m%d%H%M%S%f')) - x_0) for d in x]

                z = np.polyfit(xint, y, 1)
                p = np.poly1d(z)

                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
                plt.plot(x, y, 'go-', label='Data', linewidth=2, markersize=10)
                plt.plot(x, p(xint), 'b--', label='Fit')
                plt.legend(loc='best')
                plt.gcf().autofmt_xdate()

                plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
                plt.clf()

            elif tracker.t_type_name.tt_name in ["Duration"]:
                logs = tracker.t_logs

                if len(logs) < 3:
                    plt.annotate('Add more logs to see the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                    plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
                    plt.clf()
                    continue

                x, y = zip(*map(lambda x: (x.tl_time, int(x.tl_vals[0].tv_val)), logs))

                y = list(map(lambda t: round(t//60 + (t%60)/60, 2), y))

                x_0 = int(x[0].strftime('%Y%m%d%H%M%S%f'))
                xint = [(int(d.strftime('%Y%m%d%H%M%S%f')) - x_0) for d in x]

                z = np.polyfit(xint, y, 1)
                p = np.poly1d(z)

                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
                plt.plot(x, y, 'go-', label='Data', linewidth=2, markersize=10)
                plt.plot(x, p(xint), 'b--', label='Fit')
                plt.legend(loc='best')
                plt.gcf().autofmt_xdate()

                plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
                plt.clf()

            elif tracker.t_type_name.tt_name in ["Single Select", "Multi Select"]:
                options = {x.to_id: x.to_name for x in tracker.t_options}
                logs = tracker.t_logs

                if len(logs) < 1:
                    plt.annotate('Add more logs to see the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                    plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
                    plt.clf()
                    continue

                d = {}
                for log in logs:
                    for val in log.tl_vals:
                        if options[int(val.tv_val)] not in d:
                            d[options[int(val.tv_val)]] = 0
                        d[options[int(val.tv_val)]] += 1

                x, y = zip(*map(lambda x: (x, d[x]), d.keys()))

                patches, texts, _ = plt.pie(y, autopct='%1.0f%%')
                plt.legend(patches, x, loc='upper right', bbox_to_anchor=(1.2, 1.))

                plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
                plt.clf()

            else:
                plt.annotate('Graph not available for this type.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
                plt.clf()
        except:
            plt.annotate('Error while plotting the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
            plt.savefig(f"static/userdata/dashboard/graphs/{current_user.id}/{tracker.t_id}_main.png")
            plt.clf()

    return render_template("dashboard/dashboard.html", user=current_user, trackers=trackers, export_options=export_options)


@app.route("/trackers", methods=["GET"])
@login_required
def trackers():
    # trackers = TrackerModel.query.filter(TrackerModel.t_user == current_user.id).all()
    trackers = TrackerModel.query.filter(TrackerModel.t_user == current_user.id).order_by(nullsfirst(desc(db.session.query(TrackerLogs.tl_time).filter(TrackerLogs.tl_tracker == TrackerModel.t_id).order_by(desc(TrackerLogs.tl_time))))).all()
    return render_template("trackers/trackers.html", user=current_user, trackers=trackers)


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
        if not (action.isdigit() and int(action) in [1, 2, 3]):
            flash("Invalid Request", "danger")
            return redirect(request.full_path)
        action = int(action)

        if action == 1:
            db.session.delete(tracker)
            db.session.commit()
            flash("Tracker Deleted", "success")
            return redirect("/trackers")

        elif action == 2:
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
                tl_val = request.form.get("tl_val", "")
                try:
                    tl_val = int(float(tl_val))
                except ValueError:
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)

                tl_vals = [tl_val]

            elif tt_name in ["Decimal"]:
                tl_val = request.form.get("tl_val", "")
                try:
                    tl_val = round(float(tl_val), 2)
                except ValueError:
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)

                tl_vals = [tl_val]

            elif tt_name in ["Duration"]:
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
                tl_val = request.form.get("tl_val", "")
                to_ids = list(map(lambda x: x.to_id, tracker.t_options))
                if not (tl_val.isdigit() and int(tl_val) in to_ids):
                    flash("Invalid Value", "danger")
                    return redirect(request.full_path)
                tl_val = int(tl_val)

                tl_vals = [tl_val]

            elif tt_name in ["Multi Select"]:
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

        elif action == 3:
            tl_id = request.form.get("tl_id", "")
            if not (tl_id.isdigit()):
                flash("Invalid Log", "danger")
                return redirect(request.full_path)
            tl_id = int(tl_id)

            log = TrackerLogs.query.filter(TrackerLogs.tl_id == tl_id, TrackerLogs.tl_tracker == t_id).first()

            if not log:
                flash("Invalid Log", "danger")
                return redirect(request.full_path)

            db.session.delete(log)
            db.session.commit()
            flash(f"Log Deleted", "info")

            return redirect(request.full_path)

    options = {x.to_id: x.to_name for x in tracker.t_options}

    return render_template("trackers/view.html", user=current_user, tracker=tracker, options=options)


@app.route("/trackers/log/edit", methods=["GET", "POST"])
@login_required
def trackers_log_edit():
    t_id = request.args.get("tid", "")
    if not (t_id.isdigit()):
        flash("Invalid Log", "danger")
        return redirect("/trackers")
    t_id = int(t_id)

    tl_id = request.args.get("lid", "")
    if not (tl_id.isdigit()):
        flash("Invalid Log", "danger")
        return redirect("/trackers")
    tl_id = int(tl_id)

    tracker = TrackerModel.query.filter(TrackerModel.t_id == t_id, TrackerModel.t_user == current_user.id).first()

    if not tracker:
        flash("Invalid Log", "danger")
        return redirect("/trackers")

    log = TrackerLogs.query.filter(TrackerLogs.tl_id == tl_id, TrackerLogs.tl_tracker == t_id).first()

    if not log:
        flash("Invalid Log", "danger")
        return redirect("/trackers")

    if request.method == "POST":
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
            tl_val = request.form.get("tl_val", "")
            if tl_val == "1":
                tl_val = 1
            elif tl_val == "0":
                tl_val = 0
            else:
                flash("Invalid Value", "danger")
                return redirect(request.full_path)

            log.tl_time = tl_time
            log.tl_note = tl_note
            log.tl_vals[0].tv_val = tl_val
            db.session.commit()

        elif tt_name in ["Integer"]:
            tl_val = request.form.get("tl_val", "")
            try:
                tl_val = int(float(tl_val))
            except ValueError:
                flash("Invalid Value", "danger")
                return redirect(request.full_path)

            log.tl_time = tl_time
            log.tl_note = tl_note
            log.tl_vals[0].tv_val = tl_val
            db.session.commit()

        elif tt_name in ["Decimal"]:
            tl_val = request.form.get("tl_val", "")
            try:
                tl_val = round(float(tl_val), 2)
            except ValueError:
                flash("Invalid Value", "danger")
                return redirect(request.full_path)

            log.tl_time = tl_time
            log.tl_note = tl_note
            log.tl_vals[0].tv_val = tl_val
            db.session.commit()

        elif tt_name in ["Duration"]:
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
            
            log.tl_time = tl_time
            log.tl_note = tl_note
            log.tl_vals[0].tv_val = tl_val
            db.session.commit()

        elif tt_name in ["Single Select"]:
            tl_val = request.form.get("tl_val", "")
            to_ids = list(map(lambda x: x.to_id, tracker.t_options))
            if not (tl_val.isdigit() and int(tl_val) in to_ids):
                flash("Invalid Value", "danger")
                return redirect(request.full_path)
            tl_val = int(tl_val)

            log.tl_time = tl_time
            log.tl_note = tl_note
            log.tl_vals[0].tv_val = tl_val
            db.session.commit()

        elif tt_name in ["Multi Select"]:
            tl_vals = []
            to_ids = list(map(lambda x: x.to_id, tracker.t_options))
            for i in to_ids:
                tl_val = request.form.get(f"tl_val[{i}]", "")
                if tl_val in ["1", "on"]:
                    tl_vals.append(i)
            if len(tl_vals) == 0:
                flash("You must select at least one value", "info")
                return redirect(request.full_path)

            tl_vals_exist = list(map(lambda x: int(x.tv_val), log.tl_vals))
            tl_vals_del = list(filter(lambda x: x not in tl_vals, tl_vals_exist))
            tl_vals_add = list(filter(lambda x: x not in tl_vals_exist, tl_vals))

            log.tl_time = tl_time
            log.tl_note = tl_note

            for value in log.tl_vals:
                if value.tv_val in tl_vals_del:
                    db.session.delete(value)

            for tl_val in tl_vals_add:
                val = TrackerValues(tv_val=tl_val, tv_log=log.tl_id)
                db.session.add(val)

            db.session.commit()

        flash("Log Edited", "success")

        return redirect(f"/trackers/view?id={t_id}")

    tt_name = tracker.t_type_name.tt_name

    if tt_name == "Multi Select":
        tl_vals = list(map(lambda x: int(x.tv_val), log.tl_vals))
    else:
        tl_vals = []

    return render_template("trackers/edit_log.html", user=current_user, tracker=tracker, log=log, tl_vals=tl_vals)


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
            tracker.t_name = t_name
            tracker.t_desc = t_desc
            db.session.commit()

        elif tt_name in ["Integer", "Decimal"]:
            t_unit = request.form.get("t_unit", "")
            if not (0 < len(t_unit) <= 16):
                flash("Invalid Tracker Unit", "danger")
                return redirect(request.full_path)

            tracker.t_name = t_name
            tracker.t_desc = t_desc
            unit = TrackerUnit.query.filter(TrackerUnit.tu_tracker == t_id).one()
            unit.tu_name = t_unit
            db.session.commit()

        elif tt_name in ["Duration"]:
            tracker.t_name = t_name
            tracker.t_desc = t_desc
            db.session.commit()

        elif tt_name in ["Single Select", "Multi Select"]:
            to_ids = list(map(lambda x: x.to_id, tracker.t_options))
            to_ids_del = []
            to_ids_edit = {}
            for i in to_ids:
                t_option = request.form.get(f"t_option_exist[{i}]", "")
                if t_option == "":
                    to_ids_del.append(i)
                    continue
                if not (len(t_option) <= 64):
                    flash("Invalid Tracker Options", "danger")
                    return redirect(request.full_path)
                else:
                    to_ids_edit[i] = t_option

            to_total = request.form.get("to_total", "")
            if not (to_total.isdigit() and int(to_total) >= 0):
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

            if not (len(to_ids) - len(to_ids_del) + len(t_options) > 0):
                flash("Tracker must havet at least one option", "info")
                return redirect(request.full_path)

            tracker.t_name = t_name
            tracker.t_desc = t_desc

            for i, j in to_ids_edit.items():
                option = TrackerOptions.query.filter(TrackerOptions.to_id == i).one()
                option.to_name = j

            for i in range(len(t_options)):
                option = TrackerOptions(to_name=t_options[i], to_tracker=t_id)
                db.session.add(option)

            db.session.commit()

            if tt_name == "Single Select":
                flash("[Delete Single Select Option] This feature will be added soon!", "info")
                # Delete all logs of type "Single Select" having int(log.t_vals[0]) in to_ids_del
                # Delete all options with ids in to_ids_del
                # for i in to_ids_del:
                #     # Handle Logs -> CASCADE?
                #     option = TrackerOptions.query.filter(TrackerOptions.to_id == i).one()
                #     db.session.delete(option)
                # db.session.commit()
            elif tt_name == "Multi Select":
                flash("[Delete Multi Select Option] This feature will be added soon!", "info")
                # Delete all logs of type "Multi Select" having all int(log.t_vals) in to_ids_del
                # Delete all values with int(value) in to_ids_del
                # Delete all options with ids in to_ids_del

            # return redirect(request.full_path) # Temp (Delete this line later)

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
            tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=current_user.id)
            db.session.add(tracker)
            db.session.commit()

        elif tt_name in ["Integer", "Decimal"]:
            t_unit = request.form.get("t_unit", "")
            if not (0 < len(t_unit) <= 16):
                flash("Invalid Tracker Unit", "danger")
                return redirect(request.full_path)

            tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=current_user.id)
            db.session.add(tracker)
            db.session.commit()
            unit = TrackerUnit(tu_name=t_unit, tu_tracker=tracker.t_id)
            db.session.add(unit)
            db.session.commit()

        elif tt_name in ["Duration"]:
            tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=current_user.id)
            db.session.add(tracker)
            db.session.commit()

        elif tt_name in ["Single Select", "Multi Select"]:
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
    if current_user.is_authenticated:
        logout_user()
        flash("Logged out successfully", "info")
    return redirect(request.args.get("next", "/"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(request.args.get("next", "/"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not (4 <= len(username) <= 64):
            flash("Invalid Username", "info")
            return redirect(request.full_path)

        if not (4 <= len(password) <= 64):
            flash("Invalid Password", "info")
            return redirect(request.full_path)

        if UserModel.query.filter_by(username=username).first():
            flash("Username Not Available", "info")
            return redirect(request.full_path)

        user = UserModel(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        tokens = APIToken.query.all()
        tokens = list(map(lambda x: x.api_token, tokens))
        token = os.urandom(32).hex()
        while token in tokens:
            token = os.urandom(32).hex()
        api_token = APIToken(api_token=token, api_user=user.id)
        db.session.add(api_token)
        db.session.commit()
        login_user(user)
        flash("Registered successfully", "info")
        return redirect(request.args.get("next", "/"))

    return render_template("auth/register.html", user=current_user, request=request)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get("next", "/"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = UserModel.query.filter_by(username=username).first()
        if 4 <= len(username) <= 64 and user is not None and user.check_password(password):
            login_user(user)
            flash("Logged in successfully", "info")
            return redirect(request.args.get("next", "/"))
        else:
            flash("Invalid Credentials", "info")
            return redirect(request.full_path)

    return render_template("auth/login.html", user=current_user, request=request)
