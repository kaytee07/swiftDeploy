#!/usr/bin/pyhton3
"""
main flask app
"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

session_key = getenv('SD_SESSION_KEY')

app.secret_key = session_key

@app.teardown_appcontext
def close_storage(error):
    """
    close storage when app is torn down
    """
    SD_ENV = getenv('SD_ENV')
    if SD_ENV == 'db':
        storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return {"error": " Not found"}


if __name__ == "__main__":
    host = getenv('SD_API_HOST')
    port = getenv('SD_API_PORT')
    app.run(host=host, port=port, threaded=True)
