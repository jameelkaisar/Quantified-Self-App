from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import current_app as app

from models.models import MODEL_NAME

@app.route("/", methods=["GET"])
def home():
    return "Quantified Self Homepage"
