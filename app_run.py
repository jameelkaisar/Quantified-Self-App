from flask import Flask

from config.config import DevConfig
from database.database import db

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
app.app_context().push()

from views.views import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
