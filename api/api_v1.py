import sys

sys.path.append("../models")
sys.path.append("../database")


from models.models import UserModel
from models.models import TrackerModel, TrackerTypes, TrackerUnit, TrackerOptions
from models.models import TrackerLogs, TrackerValues
from database.database import db

from flask import current_app as app
from flask_restful import Resource, Api


class TestAPI(Resource):
    def get(self):
        return {"message": "API is working"}


api = Api(app)

api.add_resource(TestAPI, "/api/v1/test")
