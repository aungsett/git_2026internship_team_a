from flask import Flask, render_template, request, redirect, session
from backend.app.config.database import init_db
from backend.app.routes.applicant_routes import applicant_bp
from backend.app.routes.admin_routes import bp as admin_bp
import os


def create_app():
    app = Flask(
        __name__,
        template_folder="../../frontend",
        static_folder="../../frontend"
    )

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me-please")

    # Initialize database
    init_db()

    # Register API blueprints
    app.register_blueprint(applicant_bp)
    app.register_blueprint(admin_bp)

    # ----------------------------
    # FRONTEND PAGE ROUTES
    # ----------------------------

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/apply")
    def apply_page():
        return render_template("application_form.html")

    # ----------------------------
    # ADMIN LOGIN (TEMPORARY)
    # ----------------------------

    @app.route("/admin-login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if username == "admin" and password == "admin":
                session["admin_logged_in"] = True
                return redirect("/admin-dashboard")
            else:
                return render_template("admin_login.html", error=True)

        return render_template("admin_login.html", error=False)

    @app.route("/admin-dashboard")
    def admin_dashboard():
        if not session.get("admin_logged_in"):
            return redirect("/admin-login")

        return render_template("admin_dashboard.html")

    @app.route("/admin-logout")
    def admin_logout():
        session.pop("admin_logged_in", None)
        return redirect("/")

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)