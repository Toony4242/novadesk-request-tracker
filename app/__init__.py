import logging
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()
login_manager = LoginManager()


def configure_logging(app: Flask) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s %(message)s",
    )
    app.logger.setLevel(logging.INFO)
    app.logger.info("NovaDesk application configured")


def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object or Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    configure_logging(app)

    from app.auth import auth_bp
    from app.routes import main_bp
    from app.monitoring import monitoring_bp
    from app.errors import register_error_handlers

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(monitoring_bp)
    register_error_handlers(app)

    return app
