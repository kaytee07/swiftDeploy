#!/usr/bin/pyhton3
"""
main flask app
"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage():
    """
    close storage when app is torn down
    """
    storage.close()


if __name__ == "__main__":
    host = getenv('SD_API_HOST')
    port = getenv('SD_API_PORT')
    app.run(host=host, port=port, threaded=true)
