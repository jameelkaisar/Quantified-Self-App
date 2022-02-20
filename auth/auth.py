import sys
sys.path.append("../models")


from models.models import UserModel

from flask_login import LoginManager


login = LoginManager()


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
