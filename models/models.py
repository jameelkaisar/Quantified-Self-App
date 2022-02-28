import sys
sys.path.append("../database")


from database.database import db

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin


class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    user_token = db.relationship("APIToken", cascade="all, delete", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class APIToken(db.Model):
    __tablename__ = "tokens"

    api_token = db.Column(db.String(64), primary_key=True)
    api_user = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


# Temperature, Exercises
class TrackerModel(db.Model):
    __tablename__ = "trackers"

    t_id = db.Column(db.Integer(), primary_key=True)
    t_name = db.Column(db.String(64), nullable=False)
    t_desc = db.Column(db.String(256))
    t_type = db.Column(db.Integer(), db.ForeignKey("tracker_types.tt_id", ondelete="CASCADE"), nullable=False)
    t_user = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    t_type_name = db.relationship("TrackerTypes", uselist=False)
    t_unit = db.relationship("TrackerUnit", cascade="all, delete", uselist=False)
    t_options = db.relationship("TrackerOptions", cascade="all, delete")
    t_logs = db.relationship("TrackerLogs", order_by="desc(TrackerLogs.tl_time)", cascade="all, delete")


# Numerical, Multi Select
class TrackerTypes(db.Model):
    __tablename__ = "tracker_types"

    tt_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tt_name = db.Column(db.String(64), unique=True, nullable=False)


# Metre, Kilogram, Celcius, Farenheit
class TrackerUnit(db.Model):
    __tablename__ = "tracker_unit"

    tu_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tu_name = db.Column(db.String(16), nullable=False)
    tu_tracker = db.Column(db.Integer(), db.ForeignKey("trackers.t_id", ondelete="CASCADE"), nullable=False)


# Arm Exercise, Back Exercise, Neck Exercise
class TrackerOptions(db.Model):
    __tablename__ = "tracker_options"

    to_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    to_name = db.Column(db.String(64), nullable=False)
    to_tracker = db.Column(db.Integer(), db.ForeignKey("trackers.t_id", ondelete="CASCADE"), nullable=False)


# Logs (Get tl_val by using trackers.t_type.tt_name)
class TrackerLogs(db.Model):
    __tablename__ = "tracker_logs"

    tl_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tl_time = db.Column(db.DateTime(), nullable=False)
    tl_note = db.Column(db.String(256))
    tl_tracker = db.Column(db.Integer(), db.ForeignKey("trackers.t_id", ondelete="CASCADE"), nullable=False)

    tl_vals = db.relationship("TrackerValues", cascade="all, delete")


# Tracker Log Values
class TrackerValues(db.Model):
    __tablename__ = "tracker_vals"

    tv_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tv_val = db.Column(db.Numeric(10, 2), nullable=False)
    tv_log = db.Column(db.Integer(), db.ForeignKey("tracker_logs.tl_id", ondelete="CASCADE"), nullable=False)
