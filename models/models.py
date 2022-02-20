import sys
sys.path.append("../database")

from database.database import db

class MODEL_NAME(db.Model):
    __tablename__ = 'name'
    pk_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
