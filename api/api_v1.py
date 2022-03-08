import sys

sys.path.append("../models")
sys.path.append("../database")


from models.models import UserModel
from models.models import TrackerModel, TrackerTypes, TrackerUnit, TrackerOptions
from models.models import TrackerLogs, TrackerValues
from models.models import APIToken
from database.database import db

from flask import current_app as app
from flask import url_for
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_restful import fields, marshal

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from datetime import datetime
from pathlib import Path


class TestAPI(Resource):
    def get(self):
        try:
            return {"message": "API is working"}, 200

        except:
            return {"message": "Server Error"}, 500


class CheckTokenAPI(Resource):
    def __init__(self):
        self.check_token_parser = reqparse.RequestParser()
        self.check_token_parser.add_argument("APIToken", location="headers", type=str, required=True)

    def get(self):
        args = self.check_token_parser.parse_args()
        try:
            api_token = args.get("APIToken", None)
            if api_token == None:
                return {"message": "\"APIToken\" is missing"}, 401
            token = APIToken.query.filter(APIToken.api_token == api_token).first()
            if not token:
                return {"message": "Invalid Token"}, 401

            return {"message": "Valid Token"}, 200

        except:
            return {"message": "Server Error"}, 500


class GetTrackerTypesAPI(Resource):
    def __init__(self):
        self.get_tracker_types_parser = reqparse.RequestParser()
        self.get_tracker_types_parser.add_argument("APIToken", location="headers", type=str, required=True)

        self.get_tracker_types_fields = {
            "tracker_type_id": fields.Integer(attribute="tt_id"),
            "tracker_type_name": fields.String(attribute="tt_name")
        }

    def get(self):
        args = self.get_tracker_types_parser.parse_args()
        try:
            api_token = args.get("APIToken", None)
            if api_token == None:
                return {"message": "\"APIToken\" is missing"}, 401
            token = APIToken.query.filter(APIToken.api_token == api_token).first()
            if not token:
                return {"message": "Invalid Token"}, 401

            types = TrackerTypes.query.all()
            return marshal(types, self.get_tracker_types_fields), 200

        except:
            return {"message": "Server Error"}, 500


class TrackerOptionsField(fields.Raw):
    def format(self, value):
        options = list(map(lambda x: {"option_id": x.to_id, "option_name": x.to_name}, value))
        return options

class GetTrackersAPI(Resource):
    def __init__(self):
        self.get_trackers_parser = reqparse.RequestParser()
        self.get_trackers_parser.add_argument("APIToken", location="headers", type=str, required=True)

        self.get_trackers_fields = {
            "tracker_id": fields.Integer(attribute="t_id"),
            "tracker_name": fields.String(attribute="t_name"),
            "tracker_description": fields.String(attribute="t_desc"),
            "tracker_type_id": fields.Integer(attribute="t_type"),
            "tracker_type_name": fields.String(attribute="t_type_name.tt_name"),
            "tracker_unit": fields.String(attribute="t_unit.tu_name", default=None),
            "tracker_options": TrackerOptionsField(attribute="t_options")
        }

    def get(self):
        args = self.get_trackers_parser.parse_args()
        try:
            api_token = args.get("APIToken", None)
            if api_token == None:
                return {"message": "\"APIToken\" is missing"}, 401
            token = APIToken.query.filter(APIToken.api_token == api_token).first()
            if not token:
                return {"message": "Invalid Token"}, 401
            user_id = token.api_user

            trackers = TrackerModel.query.filter(TrackerModel.t_user == user_id).all()
            return marshal(trackers, self.get_trackers_fields), 200

        except:
            return {"message": "Server Error"}, 500


class LogValuesField(fields.Raw):
    def format(self, value):
        tl_tracker = value[0]
        tl_vals = value[1]

        tracker = TrackerModel.query.filter(TrackerModel.t_id == tl_tracker).one()
        tt_name = tracker.t_type_name.tt_name

        if tt_name in ["Boolean"]:
            return "Yes" if (int(tl_vals[0].tv_val) == 1) else "No"

        elif tt_name in ["Integer"]:
            return int(tl_vals[0].tv_val)

        elif tt_name in ["Decimal"]:
            return float(round(tl_vals[0].tv_val, 2))

        elif tt_name in ["Duration"]:
            return {
                "hours": int(tl_vals[0].tv_val // 3600),
                "minutes": int((tl_vals[0].tv_val % 3600) // 60),
                "seconds": int(tl_vals[0].tv_val % 60)
            }

        elif tt_name in ["Single Select"]:
            options = {x.to_id: x.to_name for x in tracker.t_options}
            return {
                "option_id": int(tl_vals[0].tv_val),
                "option_name": options[int(tl_vals[0].tv_val)]
            }

        elif tt_name in ["Multi Select"]:
            options = {x.to_id: x.to_name for x in tracker.t_options}
            selected = []
            for tl_val in tl_vals:
                selected.append({
                        "option_id": int(tl_val.tv_val),
                        "option_name": options[int(tl_val.tv_val)]
                    })
            return selected

class GetLogsAPI(Resource):
    def __init__(self):
        self.get_logs_parser = reqparse.RequestParser()
        self.get_logs_parser.add_argument("APIToken", location="headers", type=str, required=True)

        self.get_logs_fields = {
            "log_id": fields.Integer(attribute="tl_id"),
            "log_time": fields.String(attribute=lambda x: x.tl_time.strftime("%Y-%m-%d %H:%M")),
            "log_note": fields.String(attribute="tl_note"),
            "log_value": LogValuesField(attribute=lambda x: (x.tl_tracker, x.tl_vals))
        }

    def get(self, tid):
        args = self.get_logs_parser.parse_args()
        try:
            api_token = args.get("APIToken", None)
            if api_token == None:
                return {"message": "\"APIToken\" is missing"}, 401
            token = APIToken.query.filter(APIToken.api_token == api_token).first()
            if not token:
                return {"message": "Invalid Token"}, 401
            user_id = token.api_user

            if not (tid.isdigit()):
                return {"message": "Invalid Tracker ID"}, 400
            tid = int(tid)

            tracker = TrackerModel.query.filter(TrackerModel.t_id == tid, TrackerModel.t_user == user_id).first()
            if not tracker:
                return {"message": "Invalid Tracker ID"}, 400
            return marshal(tracker.t_logs, self.get_logs_fields), 200

        except:
            return {"message": "Server Error"}, 500


class GetStatsAPI(Resource):
    def __init__(self):
        self.get_stats_parser = reqparse.RequestParser()
        self.get_stats_parser.add_argument("APIToken", location="headers", type=str, required=True)

    def get(self, tid):
        args = self.get_stats_parser.parse_args()
        try:
            api_token = args.get("APIToken", None)
            if api_token == None:
                return {"message": "\"APIToken\" is missing"}, 401
            token = APIToken.query.filter(APIToken.api_token == api_token).first()
            if not token:
                return {"message": "Invalid Token"}, 401
            user_id = token.api_user

            if not (tid.isdigit()):
                return {"message": "Invalid Tracker ID"}, 400
            tid = int(tid)

            tracker = TrackerModel.query.filter(TrackerModel.t_id == tid, TrackerModel.t_user == user_id).first()
            if not tracker:
                return {"message": "Invalid Tracker ID"}, 400

            Path(f"static/userdata/dashboard/graphs/{user_id}/").mkdir(parents=True, exist_ok=True)

            try:
                if tracker.t_type_name.tt_name in ["Boolean"]:
                    logs = tracker.t_logs

                    if len(logs) < 1:
                        plt.annotate('Add more logs to see the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                        plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                        plt.clf()

                    else:
                        x = ["Yes", "No"]
                        y = [sum(map(lambda x: int(x.tl_vals[0].tv_val), logs))]
                        y.append(len(logs) - y[0])

                        patches, texts, _ = plt.pie(y, autopct='%1.0f%%')
                        plt.legend(patches, x, loc='upper right', bbox_to_anchor=(1.2, 1.))

                        plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                        plt.clf()

                elif tracker.t_type_name.tt_name in ["Integer", "Decimal"]:
                    logs = tracker.t_logs

                    if len(logs) < 3:
                        plt.annotate('Add more logs to see the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                        plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                        plt.clf()

                    else:
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

                        plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                        plt.clf()

                elif tracker.t_type_name.tt_name in ["Duration"]:
                    logs = tracker.t_logs

                    if len(logs) < 3:
                        plt.annotate('Add more logs to see the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                        plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                        plt.clf()

                    else:
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

                        plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                        plt.clf()

                elif tracker.t_type_name.tt_name in ["Single Select", "Multi Select"]:
                    options = {x.to_id: x.to_name for x in tracker.t_options}
                    logs = tracker.t_logs

                    if len(logs) < 1:
                        plt.annotate('Add more logs to see the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                        plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                        plt.clf()

                    else:
                        d = {}
                        for log in logs:
                            for val in log.tl_vals:
                                if options[int(val.tv_val)] not in d:
                                    d[options[int(val.tv_val)]] = 0
                                d[options[int(val.tv_val)]] += 1

                        x, y = zip(*map(lambda x: (x, d[x]), d.keys()))

                        patches, texts, _ = plt.pie(y, autopct='%1.0f%%')
                        plt.legend(patches, x, loc='upper right', bbox_to_anchor=(1.2, 1.))

                        plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                        plt.clf()

                else:
                    plt.annotate('Graph not available for this type.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                    plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                    plt.clf()
            except:
                plt.annotate('Error while plotting the graph.', (0.5, 0.5), xycoords='axes fraction', va='center', ha='center')
                plt.savefig(f"static/userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")
                plt.clf()

            stats_url = url_for("static", filename=f"userdata/dashboard/graphs/{user_id}/{tracker.t_id}_main.png")

            return {"tracker_stats_url": stats_url}, 200

        except:
            return {"message": "Server Error"}, 500


class AddTrackerAPI(Resource):
    def __init__(self):
        self.add_tracker_parser = reqparse.RequestParser()
        self.add_tracker_parser.add_argument("APIToken", location="headers", type=str, required=True)
        self.add_tracker_parser.add_argument("tracker_name", type=str, required=True, help="\"tracker_name\" is missing")
        self.add_tracker_parser.add_argument("tracker_description", type=str, default="", help="\"tracker_description\" is missing")
        self.add_tracker_parser.add_argument("tracker_type_id", type=str, required=True, help="\"tracker_type_id\" is missing")
        self.add_tracker_parser.add_argument("tracker_unit", type=str)
        self.add_tracker_parser.add_argument("tracker_options", type=str, action="append")

    def post(self):
        args = self.add_tracker_parser.parse_args()
        try:
            api_token = args.get("APIToken", None)
            t_name = args.get("tracker_name", "")
            t_desc = args.get("tracker_description", "")
            t_type = args.get("tracker_type_id", "")

            if api_token == None:
                return {"message": "\"APIToken\" is missing"}, 401
            token = APIToken.query.filter(APIToken.api_token == api_token).first()
            if not token:
                return {"message": "Invalid Token"}, 401
            user_id = token.api_user

            if not (0 < len(t_name) <= 64):
                return {"message": "Invalid Tracker Name"}, 400

            if not (0 <= len(t_desc) <= 256):
                return {"message": "Invalid Tracker Description"}, 400

            tracker_types = TrackerTypes.query.all()
            if not (t_type.isdigit() and int(t_type) in map(lambda x: x.tt_id, tracker_types)):
                return {"message": "Invalid Tracker Type ID"}, 400
            t_type = int(t_type)

            tt_id = t_type
            tt_name = list(filter(lambda x: x.tt_id == tt_id, tracker_types))[0].tt_name

            if tt_name in ["Boolean"]:
                tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=user_id)
                db.session.add(tracker)
                db.session.commit()
                return {"message": "Tracker Added Successfully", "tracker_id": tracker.t_id}, 200

            elif tt_name in ["Integer", "Decimal"]:
                t_unit = args.get("tracker_unit", None)
                if t_unit == None:
                    return {"message": "\"tracker_unit\" is missing"}, 400
                if not (0 < len(t_unit) <= 16):
                    return {"message": "Invalid Tracker Unit"}, 400

                tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=user_id)
                db.session.add(tracker)
                db.session.commit()
                unit = TrackerUnit(tu_name=t_unit, tu_tracker=tracker.t_id)
                db.session.add(unit)
                db.session.commit()
                return {"message": "Tracker Added Successfully", "tracker_id": tracker.t_id}, 200

            elif tt_name in ["Duration"]:
                tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=user_id)
                db.session.add(tracker)
                db.session.commit()
                return {"message": "Tracker Added Successfully", "tracker_id": tracker.t_id}, 200

            elif tt_name in ["Single Select", "Multi Select"]:
                t_options = args.get("tracker_options", None)
                if t_options == None:
                    return {"message": "\"tracker_options\" is missing"}, 400
                if not (len(t_options) > 0):
                    return {"message": "Invalid Tracker Options"}, 400

                for i in t_options:
                    if not (0 < len(i) <= 64):
                        return {"message": "Invalid Tracker Options"}, 400

                tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=user_id)
                db.session.add(tracker)
                db.session.commit()
                for i in t_options:
                    option = TrackerOptions(to_name=i, to_tracker=tracker.t_id)
                    db.session.add(option)
                db.session.commit()
                return {"message": "Tracker Added Successfully", "tracker_id": tracker.t_id}, 200

        except:
            return {"message": "Server Error"}, 500


class AddLogAPI(Resource):
    def __init__(self):
        self.add_log_parser = reqparse.RequestParser()
        self.add_log_parser.add_argument("APIToken", location="headers", type=str, required=True)
        self.add_log_parser.add_argument("log_time", type=str, required=True, help="\"log_time\" is missing")
        self.add_log_parser.add_argument("log_note", type=str, default="", help="\"log_note\" is missing")
        self.add_log_parser.add_argument("log_value", type=str, action="append", required=True, help="\"log_value\" is missing")

    def post(self, tid):
        args = self.add_log_parser.parse_args()
        try:
            api_token = args.get("APIToken", None)
            tl_time = args.get("log_time", "")
            tl_note = args.get("log_note", "")

            if api_token == None:
                return {"message": "\"APIToken\" is missing"}, 401
            token = APIToken.query.filter(APIToken.api_token == api_token).first()
            if not token:
                return {"message": "Invalid Token"}, 401
            user_id = token.api_user

            if not (tid.isdigit()):
                return {"message": "Invalid Tracker ID"}, 400
            tid = int(tid)

            tracker = TrackerModel.query.filter(TrackerModel.t_id == tid, TrackerModel.t_user == user_id).first()
            if not tracker:
                return {"message": "Invalid Tracker ID"}, 400

            if not (len(tl_time) == 16):
                return {"message": "Invalid Log Time"}, 400
            try:
                tl_time = datetime.strptime(tl_time, "%Y-%m-%d %H:%M")
            except ValueError:
                return {"message": "Invalid Log Time"}, 400

            if not (0 <= len(tl_note) <= 256):
                return {"message": "Invalid Log Note"}, 400

            tt_name = tracker.t_type_name.tt_name

            if tt_name in ["Boolean"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    return {"message": "Invalid Log Value"}, 400
                try:
                    tl_val = tl_val[0]
                except:
                    return {"message": "Invalid Log Value"}, 400
                if tl_val == "Yes":
                    tl_val = 1
                elif tl_val == "No":
                    tl_val = 0
                else:
                    return {"message": "Invalid Log Value"}, 400

                tl_vals = [tl_val]

            elif tt_name in ["Integer"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    return {"message": "Invalid Log Value"}, 400
                try:
                    tl_val = tl_val[0]
                    tl_val = int(float(tl_val))
                except ValueError:
                    return {"message": "Invalid Log Value"}, 400

                tl_vals = [tl_val]

            elif tt_name in ["Decimal"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    return {"message": "Invalid Log Value"}, 400
                try:
                    tl_val = tl_val[0]
                    tl_val = round(float(tl_val), 2)
                except ValueError:
                    return {"message": "Invalid Log Value"}, 400

                tl_vals = [tl_val]

            elif tt_name in ["Duration"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    return {"message": "Invalid Log Value"}, 400
                try:
                    tl_val = tl_val[0]
                except:
                    return {"message": "Invalid Log Value"}, 400
                if not (tl_val.isdigit() and 0 <= int(tl_val) <= (100*60*60 + 59*60 + 59)):
                    return {"message": "Invalid Log Value"}, 400
                tl_val = int(tl_val)

                tl_vals = [tl_val]

            elif tt_name in ["Single Select"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    return {"message": "Invalid Log Value"}, 400
                try:
                    tl_val = tl_val[0]
                except:
                    return {"message": "Invalid Log Value"}, 400
                to_ids = list(map(lambda x: x.to_id, tracker.t_options))
                if not (tl_val.isdigit() and int(tl_val) in to_ids):
                    return {"message": "Invalid Log Value"}, 400
                tl_val = int(tl_val)

                tl_vals = [tl_val]

            elif tt_name in ["Multi Select"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    return {"message": "Invalid Log Value"}, 400
                tl_vals = []
                to_ids = list(map(lambda x: x.to_id, tracker.t_options))
                for i in to_ids:
                    if str(i) in tl_val:
                        tl_vals.append(i)
                if len(tl_vals) == 0:
                    return {"message": "Invalid Log Value"}, 400

            log = TrackerLogs(tl_time=tl_time, tl_note=tl_note, tl_tracker=tracker.t_id)
            db.session.add(log)
            db.session.commit()
            for tl_val in tl_vals:
                val = TrackerValues(tv_val=tl_val, tv_log=log.tl_id)
                db.session.add(val)
            db.session.commit()
            return {"message": "Log Added Successfully", "log_id": log.tl_id}, 200

        except:
            return {"message": "Server Error"}, 500


class DeleteTrackerAPI(Resource):
    def __init__(self):
        self.delete_tracker_parser = reqparse.RequestParser()
        self.delete_tracker_parser.add_argument("APIToken", location="headers", type=str, required=True)

    def delete(self, tid):
        args = self.delete_tracker_parser.parse_args()
        try:
            api_token = args.get("APIToken", None)
            if api_token == None:
                return {"message": "\"APIToken\" is missing"}, 401
            token = APIToken.query.filter(APIToken.api_token == api_token).first()
            if not token:
                return {"message": "Invalid Token"}, 401
            user_id = token.api_user

            if not (tid.isdigit()):
                return {"message": "Invalid Tracker ID"}, 400
            tid = int(tid)

            tracker = TrackerModel.query.filter(TrackerModel.t_id == tid, TrackerModel.t_user == user_id).first()
            if not tracker:
                return {"message": "Invalid Tracker ID"}, 400

            db.session.delete(tracker)
            db.session.commit()
            return {"message": "Tracker Deleted Successfully"}, 200

        except:
            return {"message": "Server Error"}, 500


class DeleteLogAPI(Resource):
    def __init__(self):
        self.delete_log_parser = reqparse.RequestParser()
        self.delete_log_parser.add_argument("APIToken", location="headers", type=str, required=True)

    def delete(self, tid, lid):
        args = self.delete_log_parser.parse_args()
        try:
            api_token = args.get("APIToken", None)
            if api_token == None:
                return {"message": "\"APIToken\" is missing"}, 401
            token = APIToken.query.filter(APIToken.api_token == api_token).first()
            if not token:
                return {"message": "Invalid Token"}, 401
            user_id = token.api_user

            if not (tid.isdigit()):
                return {"message": "Invalid Tracker ID"}, 400
            tid = int(tid)

            tracker = TrackerModel.query.filter(TrackerModel.t_id == tid, TrackerModel.t_user == user_id).first()
            if not tracker:
                return {"message": "Invalid Tracker ID"}, 400

            if not (lid.isdigit()):
                return {"message": "Invalid Log ID"}, 400
            lid = int(lid)

            log = TrackerLogs.query.filter(TrackerLogs.tl_id == lid, TrackerLogs.tl_tracker == tid).first()
            if not log:
                return {"message": "Invalid Log ID"}, 400

            db.session.delete(log)
            db.session.commit()
            return {"message": "Log Deleted Successfully"}, 200

        except:
            return {"message": "Server Error"}, 500


api = Api(app)

api.add_resource(TestAPI, "/api/v1/test")
api.add_resource(CheckTokenAPI, "/api/v1/checkToken")

api.add_resource(GetTrackerTypesAPI, "/api/v1/getTrackerTypes")
api.add_resource(GetTrackersAPI, "/api/v1/getTrackers")
api.add_resource(GetLogsAPI, "/api/v1/getLogs/<string:tid>")
api.add_resource(GetStatsAPI, "/api/v1/getStats/<string:tid>")

api.add_resource(AddTrackerAPI, "/api/v1/addTracker")
api.add_resource(AddLogAPI, "/api/v1/addLog/<string:tid>")

api.add_resource(DeleteTrackerAPI, "/api/v1/deleteTracker/<string:tid>")
api.add_resource(DeleteLogAPI, "/api/v1/deleteLog/<string:tid>/<string:lid>")
