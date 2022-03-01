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


# add_tracker_parser = reqparse.RequestParser()
# add_tracker_parser.add_argument("name", type=str, required=True, help="Tracker name is missing")

# class AddTrackerAPI(Resource):
#     def post(self, token):
#         tokens = APIToken.query.all()
#         tokens = dict(map(lambda x: (x.api_token, x.api_user), tokens))

#         if token in tokens.keys():
#             args = add_tracker_parser.parse_args()
#             name = args.get("name")

#             return {"message": "Name is " + name}, 200

#         else:
#             abort(401, message="Invalid Token")


api = Api(app)

api.add_resource(TestAPI, "/api/v1/test")
api.add_resource(CheckTokenAPI, "/api/v1/<string:token>/checkToken")

api.add_resource(GetTrackerTypesAPI, "/api/v1/<string:token>/getTrackerTypes")
api.add_resource(GetTrackersAPI, "/api/v1/<string:token>/getTrackers")
api.add_resource(GetTrackerLogsAPI, "/api/v1/<string:token>/getTrackerLogs/<string:tid>")

# api.add_resource(AddTrackerAPI, "/api/v1/<string:token>/addTracker")
