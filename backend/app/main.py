from flask import Flask
from backend.app.config.database import init_db
from backend.app.routes.applicant_routes import bp as apply_bp
from backend.app.routes.admin_routes import bp as admin_bp

def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(apply_bp)
    app.register_blueprint(admin_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
