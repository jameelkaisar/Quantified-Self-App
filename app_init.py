from flask import Flask

import os
key = os.urandom(16).hex()
with open(".env", "w") as file:
    file.write(f"SECRET_KEY={key}\n")

from config.config import DevConfig
from database.database import db
from models.models import TrackerTypes
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
app.app_context().push()


from views.views import *


db.create_all()
db.session.commit()

types = ["Boolean", "Integer", "Decimal", "Duration", "Single Select", "Multi Select"]
for t in types:
    try:
        tracker_type = TrackerTypes(tt_name=t)
        db.session.add(tracker_type)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
