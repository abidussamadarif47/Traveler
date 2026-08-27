from flask import Flask, render_template
from flask_login import LoginManager

from config import Config
from models import db
from models.user import User

from routes.auth import auth_bp
from routes.tour import tour_bp
from routes.booking import booking_bp
from routes.admin import admin_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to access this page."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    app.register_blueprint(auth_bp)
    app.register_blueprint(tour_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        from models.tour import Tour
        tours = (
            Tour.query.filter_by(status="upcoming")
            .order_by(Tour.departure_date.asc())
            .limit(6)
            .all()
        )
        return render_template("home.html", tours=tours)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template(
            "error.html",
            error_code=403,
            message="You do not have permission to access this page."
        ), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template(
            "error.html",
            error_code=404,
            message="The page you are looking for was not found."
        ), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
