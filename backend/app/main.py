from flask import Flask
from backend.app.config.database import init_db
from backend.app.config.settings import settings

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    # initialize DB
    init_db()
    # register blueprints later...
    return app

if __name__ == "__main__":
    create_app().run(debug=(settings.FLASK_ENV == "development"))

