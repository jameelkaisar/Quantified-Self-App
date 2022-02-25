from flask import current_app as app
from humanize.time import naturaltime

@app.template_filter()
def pretty_datetime(datetime):
    return naturaltime(datetime)
