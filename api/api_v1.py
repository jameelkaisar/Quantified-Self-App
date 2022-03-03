import sys

sys.path.append("../models")
sys.path.append("../database")


from models.models import UserModel
from models.models import TrackerModel, TrackerTypes, TrackerUnit, TrackerOptions
from models.models import TrackerLogs, TrackerValues
from models.models import APIToken
from database.database import db

from flask import current_app as app
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from flask_restful import abort

from datetime import datetime


class TestAPI(Resource):
    def get(self):
        return {"message": "API is working"}, 200


class CheckTokenAPI(Resource):
    def get(self, token):
        tokens = APIToken.query.all()
        tokens = dict(map(lambda x: (x.api_token, x.api_user), tokens))

        if token in tokens.keys():
            return {"message": "Valid Token"}, 200

        else:
            abort(401, message="Invalid Token")


get_tracker_types_fields = {
    "tracker_type_id": fields.Integer(attribute="tt_id"),
    "tracker_type_name": fields.String(attribute="tt_name")
}

class GetTrackerTypesAPI(Resource):
    @marshal_with(get_tracker_types_fields)
    def get(self, token):
        tokens = APIToken.query.all()
        tokens = dict(map(lambda x: (x.api_token, x.api_user), tokens))

        if token in tokens.keys():
            types = TrackerTypes.query.all()
            return types, 200

        else:
            abort(401, message="Invalid Token")


class TrackerOptionsField(fields.Raw):
    def format(self, value):
        options = list(map(lambda x: {"option_id": x.to_id, "option_name": x.to_name}, value))
        return options

get_trackers_fields = {
    "tracker_id": fields.Integer(attribute="t_id"),
    "tracker_name": fields.String(attribute="t_name"),
    "tracker_description": fields.String(attribute="t_desc"),
    "tracker_type_id": fields.Integer(attribute="t_type"),
    "tracker_type_name": fields.String(attribute="t_type_name.tt_name"),
    "tracker_unit": fields.String(attribute="t_unit.tu_name", default=None),
    "tracker_options": TrackerOptionsField(attribute="t_options")
}

class GetTrackersAPI(Resource):
    @marshal_with(get_trackers_fields)
    def get(self, token):
        tokens = APIToken.query.all()
        tokens = dict(map(lambda x: (x.api_token, x.api_user), tokens))

        if token in tokens.keys():
            user_id = tokens[token]
            trackers = TrackerModel.query.filter(TrackerModel.t_user == user_id).all()
            return trackers, 200

        else:
            abort(401, message="Invalid Token")


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

get_logs_fields = {
    "log_id": fields.Integer(attribute="tl_id"),
    "log_time": fields.String(attribute=lambda x: x.tl_time.strftime("%Y-%m-%d %H:%M")),
    "log_note": fields.String(attribute="tl_note"),
    "log_value": LogValuesField(attribute=lambda x: (x.tl_tracker, x.tl_vals))
}

class GetTrackerLogsAPI(Resource):
    @marshal_with(get_logs_fields)
    def get(self, token, tid):
        tokens = APIToken.query.all()
        tokens = dict(map(lambda x: (x.api_token, x.api_user), tokens))

        if token in tokens.keys():
            user_id = tokens[token]

            if not (tid.isdigit()):
                abort(400, message="Invalid Tracker ID")
            tid = int(tid)

            tracker = TrackerModel.query.filter(TrackerModel.t_id == tid, TrackerModel.t_user == user_id).first()
            if not tracker:
                abort(400, message="Invalid Tracker ID")
            return tracker.t_logs, 200

        else:
            abort(401, message="Invalid Token")


add_tracker_parser = reqparse.RequestParser()
add_tracker_parser.add_argument("tracker_name", type=str, required=True, help="\"tracker_name\" is missing")
add_tracker_parser.add_argument("tracker_description", type=str, required=True, help="\"tracker_description\" is missing")
add_tracker_parser.add_argument("tracker_type_id", type=str, required=True, help="\"tracker_type_id\" is missing")
add_tracker_parser.add_argument("tracker_unit", type=str)
add_tracker_parser.add_argument("tracker_options", type=str, action="append")

class AddTrackerAPI(Resource):
    def post(self, token):
        tokens = APIToken.query.all()
        tokens = dict(map(lambda x: (x.api_token, x.api_user), tokens))

        if token in tokens.keys():
            user_id = tokens[token]

            args = add_tracker_parser.parse_args()
            t_name = args.get("tracker_name", "")
            t_desc = args.get("tracker_description", "")
            t_type = args.get("tracker_type_id", "")

            if not (0 < len(t_name) <= 64):
                abort(401, message="Invalid Tracker Name")

            if not (0 <= len(t_desc) <= 256):
                abort(401, message="Invalid Tracker Description")

            tracker_types = TrackerTypes.query.all()
            if not (t_type.isdigit() and int(t_type) in map(lambda x: x.tt_id, tracker_types)):
                abort(401, message="Invalid Tracker Type ID")
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
                    abort(401, message="\"tracker_unit\" is missing")
                if not (0 < len(t_unit) <= 16):
                    abort(401, message="Invalid Tracker Unit")

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
                    abort(401, message="\"tracker_options\" is missing")
                if not (len(t_options) > 0):
                    abort(401, message="Invalid Tracker Options")

                for i in t_options:
                    if not (0 < len(i) <= 64):
                        abort(401, message="Invalid Tracker Options")

                tracker = TrackerModel(t_name=t_name, t_desc=t_desc, t_type=tt_id, t_user=user_id)
                db.session.add(tracker)
                db.session.commit()
                for i in t_options:
                    option = TrackerOptions(to_name=i, to_tracker=tracker.t_id)
                    db.session.add(option)
                db.session.commit()
                return {"message": "Tracker Added Successfully", "tracker_id": tracker.t_id}, 200

        else:
            abort(401, message="Invalid Token")


add_log_parser = reqparse.RequestParser()
add_log_parser.add_argument("log_time", type=str, required=True, help="\"log_time\" is missing")
add_log_parser.add_argument("log_note", type=str, default="", help="\"log_note\" is missing")
add_log_parser.add_argument("log_value", type=str, action="append", required=True, help="\"log_value\" is missing")

class AddLogAPI(Resource):
    def post(self, token, tid):
        tokens = APIToken.query.all()
        tokens = dict(map(lambda x: (x.api_token, x.api_user), tokens))

        if token in tokens.keys():
            user_id = tokens[token]

            if not (tid.isdigit()):
                abort(400, message="Invalid Tracker ID")
            tid = int(tid)

            tracker = TrackerModel.query.filter(TrackerModel.t_id == tid, TrackerModel.t_user == user_id).first()
            if not tracker:
                abort(400, message="Invalid Tracker ID")

            args = add_log_parser.parse_args()
            tl_time = args.get("log_time", "")
            tl_note = args.get("log_note", "")

            if not (len(tl_time) == 16):
                abort(401, message="Invalid Log Time")
            try:
                tl_time = datetime.strptime(tl_time, "%Y-%m-%d %H:%M")
            except ValueError:
                abort(401, message="Invalid Log Time") 

            if not (0 <= len(tl_note) <= 256):
                abort(401, message="Invalid Log Note")

            tt_name = tracker.t_type_name.tt_name

            if tt_name in ["Boolean"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    abort(401, message="Invalid Log Value")
                try:
                    tl_val = tl_val[0]
                except:
                    abort(401, message="Invalid Log Value")
                if tl_val == "Yes":
                    tl_val = 1
                elif tl_val == "No":
                    tl_val = 0
                else:
                    abort(401, message="Invalid Log Value")

                tl_vals = [tl_val]

            elif tt_name in ["Integer"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    abort(401, message="Invalid Log Value")
                try:
                    tl_val = tl_val[0]
                    tl_val = int(float(tl_val))
                except ValueError:
                    abort(401, message="Invalid Log Value")

                tl_vals = [tl_val]

            elif tt_name in ["Decimal"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    abort(401, message="Invalid Log Value")
                try:
                    tl_val = tl_val[0]
                    tl_val = round(float(tl_val), 2)
                except ValueError:
                    abort(401, message="Invalid Log Value")

                tl_vals = [tl_val]

            elif tt_name in ["Duration"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    abort(401, message="Invalid Log Value")
                try:
                    tl_val = tl_val[0]
                except:
                    abort(401, message="Invalid Log Value")
                if not (tl_val.isdigit() and 0 <= int(tl_val) <= (100*60*60 + 59*60 + 59)):
                    abort(401, message="Invalid Log Value")
                tl_val = int(tl_val)

                tl_vals = [tl_val]

            elif tt_name in ["Single Select"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    abort(401, message="Invalid Log Value")
                try:
                    tl_val = tl_val[0]
                except:
                    abort(401, message="Invalid Log Value")
                to_ids = list(map(lambda x: x.to_id, tracker.t_options))
                if not (tl_val.isdigit() and int(tl_val) in to_ids):
                    abort(401, message="Invalid Log Value")
                tl_val = int(tl_val)

                tl_vals = [tl_val]

            elif tt_name in ["Multi Select"]:
                tl_val = args.get("log_value", None)
                if tl_val == None:
                    abort(401, message="Invalid Log Value")
                tl_vals = []
                to_ids = list(map(lambda x: x.to_id, tracker.t_options))
                for i in to_ids:
                    if str(i) in tl_val:
                        tl_vals.append(i)
                if len(tl_vals) == 0:
                    abort(401, message="Invalid Log Value")

            log = TrackerLogs(tl_time=tl_time, tl_note=tl_note, tl_tracker=tracker.t_id)
            db.session.add(log)
            db.session.commit()
            for tl_val in tl_vals:
                val = TrackerValues(tv_val=tl_val, tv_log=log.tl_id)
                db.session.add(val)
            db.session.commit()
            return {"message": "Log Added Successfully", "log_id": log.tl_id}, 200

        else:
            abort(401, message="Invalid Token")


api = Api(app)

api.add_resource(TestAPI, "/api/v1/test")
api.add_resource(CheckTokenAPI, "/api/v1/<string:token>/checkToken")

api.add_resource(GetTrackerTypesAPI, "/api/v1/<string:token>/getTrackerTypes")
api.add_resource(GetTrackersAPI, "/api/v1/<string:token>/getTrackers")
api.add_resource(GetTrackerLogsAPI, "/api/v1/<string:token>/getTrackerLogs/<string:tid>")

api.add_resource(AddTrackerAPI, "/api/v1/<string:token>/addTracker")
api.add_resource(AddLogAPI, "/api/v1/<string:token>/addLog/<string:tid>")
