from flask import Flask

from config.config import DevConfig
from database.database import db
from auth.auth import login


app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
login.init_app(app)
login.login_view = "login"
login.login_message = "Please log in to access this page."
login.login_message_category = "info"
app.app_context().push()


from views.views import *
from api.api_v1 import *
from templates.filters.filters import *


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
