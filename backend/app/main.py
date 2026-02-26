from flask import Flask
from backend.app.config.database import init_db
from backend.app.routes.applicant_routes import bp as apply_bp
from backend.app.routes.admin_routes import bp as admin_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    init_db()
    app.register_blueprint(apply_bp)
    app.register_blueprint(admin_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))  # dynamic port for Render
    app.run(host="0.0.0.0", port=port)
