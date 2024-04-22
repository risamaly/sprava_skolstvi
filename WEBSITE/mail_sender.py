import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
from flask_mail import Message
from flask_mail import Mail
from LOG.logging import setup_logger
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from flask import current_app

class MailSender():
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'richard.maly2005@gmail.com'
    MAIL_PASSWORD = 'iokuydaykpmncfas'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    def __init__(self, app=None):
        """Inicializuje Mailsender v ramci aplikace"""
        self.mail = None
        if app is not setup_logger('email_logger'):
            self.logger = setup_logger('email_logger')
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Inicaliazice configu v ramci aplikace"""
        app.config['MAIL_SERVER'] = self.MAIL_SERVER
        app.config['MAIL_PORT'] = self.MAIL_PORT
        app.config['MAIL_USERNAME'] = self.MAIL_USERNAME
        app.config['MAIL_PASSWORD'] = self.MAIL_PASSWORD
        app.config['MAIL_USE_TLS'] = self.MAIL_USE_TLS
        app.config['MAIL_USE_SSL'] = self.MAIL_USE_SSL
        self.mail = Mail(app)

    def generate_confirmation_token(self, email, sid):
        """Vygeneruje token"""
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps({'email': email, 'sid': sid}, salt='password-reset-salt')

    def confirm_token(self, token, expiration=3600):
        """Token s expiraci za hodinu"""
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
        except:
            return False
        return data

    def send_email(self, recipient, sid, subject="Zmena Hesla", body=""):
        """odesle eamil pro resetovani hesla"""
        if not self.mail:
            raise RuntimeError("MailSender není inicializovaný s Flaskem :(.")
        token = self.generate_confirmation_token(recipient, sid)
        reset_url = url_for('routes.reset_password', token=token, _external=True)
        message = Message(subject, sender=self.MAIL_USERNAME, recipients=[recipient])
        message.body = f"{body}\nKlinete na link pro reset helsa: {reset_url}"
        self.mail.send(message)
        self.logger.info(f"Email sent to {recipient}")

    def request_new_user(self, recipient, form_data, subject="Žádost o Přidání Nového Uživatele", body=""):
        """odelse zadost o noveho uzivatele"""
        if not self.mail:
            raise RuntimeError("MailSender není inicializovaný s Flaskem :(.")
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(form_data, salt='user-registration')
        form_url = url_for('admin_routes.request_add_user', token=token, _external=True)
        message = Message(subject, sender=self.MAIL_USERNAME, recipients=[recipient])
        message.body = f"{body}\nKlikněte zde pro přidání užiavtele: {form_url}"
        self.mail.send(message)


    def send_support_mail(self, sender_email, recipient_email, subject, body):
        """odesle eamil na podporu"""
        if not self.mail:
            raise RuntimeError("MailSender není inicializovaný s Flaskem :(.")
        
        message = Message(subject, sender=sender_email, recipients=[recipient_email])
        message.body = body
        try:
            self.mail.send(message)
            self.logger.info(f"Support email sent from {sender_email} to {recipient_email}")
        except Exception as e:
            self.logger.error(f"Error sending support email from {sender_email} to {recipient_email}: {e}")
            raise


