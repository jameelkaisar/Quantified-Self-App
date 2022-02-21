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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Temperature, Exercises
class TrackerModel(db.Model):
    __tablename__ = "trackers"

    t_id = db.Column(db.Integer(), primary_key=True)
    t_name = db.Column(db.String(64), nullable=False)
    t_desc = db.Column(db.String(256))
    t_type = db.Column(db.Integer(), db.ForeignKey("tracker_types.tt_id", ondelete="CASCADE"), nullable=False)
    t_user = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


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


# Boolean Values
class TrackerValueBool(db.Model):
    __tablename__ = "tracker_val_bool"

    tv_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tv_val = db.Column(db.Boolean(), nullable=False)
    tv_log = db.Column(db.Integer(), db.ForeignKey("tracker_logs.tl_id", ondelete="CASCADE"), nullable=False)


# Numerical Values (Duration/Integer/Float)
class TrackerValueNum(db.Model):
    __tablename__ = "tracker_val_num"

    tv_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tv_val = db.Column(db.Numeric(10, 2), nullable=False)
    tv_log = db.Column(db.Integer(), db.ForeignKey("tracker_logs.tl_id", ondelete="CASCADE"), nullable=False)


# Single Select Values
class TrackerValueSin(db.Model):
    __tablename__ = "tracker_val_sin"

    tv_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tv_val = db.Column(db.Integer(), db.ForeignKey("tracker_options.to_id"), nullable=False)
    tv_log = db.Column(db.Integer(), db.ForeignKey("tracker_logs.tl_id", ondelete="CASCADE"), nullable=False)


# Multi Select
class TrackerValueMul(db.Model):
    __tablename__ = "tracker_val_mul"

    tv_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tv_log = db.Column(db.Integer(), db.ForeignKey("tracker_logs.tl_id", ondelete="CASCADE"), nullable=False)


# Multi Select Values
class TrackerValueMulOpts(db.Model):
    __tablename__ = "tracker_val_mul_opts"

    tvo_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tvo_val = db.Column(db.Integer(), db.ForeignKey("tracker_options.to_id"), nullable=False)
    tvo_mul = db.Column(db.Integer(), db.ForeignKey("tracker_val_mul.tv_id", ondelete="CASCADE"), nullable=False)

