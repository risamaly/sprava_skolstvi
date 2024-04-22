from flask import Flask
from DATABASE.database_config import Database_Config
from flask_mysqldb import MySQL
from LOG.logging import setup_logger
from WEBSITE.mail_sender import MailSender

def create_flask_app():
    """Vytváří flask aplikaci"""
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = "jecna"

    logger = setup_logger('database_logger', 'database.log')

    dc = Database_Config()
    is_connected = dc.test_connections()

    if is_connected == True:
        flask_app.config["MYSQL_HOST"] = dc.MYSQL_HOST
        flask_app.config["MYSQL_USER"] = dc.MYSQL_USER
        flask_app.config["MYSQL_PASSWORD"] = dc.MYSQL_PASSWORD
        flask_app.config["MYSQL_DB"] = dc.MYSQL_DATABASE

        flask_app.mysql = MySQL(flask_app)
    else:
        logger.error(f"Chyba při připojování k databázi")

    mail_sender = MailSender()

    flask_app.mail_sender = mail_sender

    flask_app.config['MAIL_SERVER'] = mail_sender.MAIL_SERVER
    flask_app.config['MAIL_PORT'] = mail_sender.MAIL_PORT
    flask_app.config['MAIL_USERNAME'] = mail_sender.MAIL_USERNAME
    flask_app.config['MAIL_PASSWORD'] = mail_sender.MAIL_PASSWORD
    flask_app.config['MAIL_USE_TLS'] = mail_sender.MAIL_USE_TLS
    flask_app.config['MAIL_USE_SSL'] = mail_sender.MAIL_USE_SSL

    mail_sender.init_app(flask_app)

    from WEBSITE.routes import routes
    from WEBSITE.authentication_routes import authentication_routes
    from WEBSITE.admin_routes import admin_routes
    from WEBSITE.user_routes import user_routes
    from WEBSITE.student_routes import student_routes
    from WEBSITE.secret import secret
    flask_app.register_blueprint(admin_routes, url_prefix="/")
    flask_app.register_blueprint(routes, url_prefix='/')
    flask_app.register_blueprint(authentication_routes, url_prefix='/')
    flask_app.register_blueprint(user_routes, url_prefix='/')
    flask_app.register_blueprint(student_routes, url_prefix='/')
    flask_app.register_blueprint(secret, url_prefix='/secret')

    return flask_app