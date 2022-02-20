from flask import Flask

from config.config import DevConfig
from database.database import db


app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
app.app_context().push()


from views.views import *


db.create_all()
db.session.commit()
