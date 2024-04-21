import unittest
from unittest.mock import patch, Mock
from flask import Flask
from WEBSITE import MailSender 

class TestMailSender(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'super-secret-key'
        self.mail_sender = MailSender(self.app)

    @patch('your_mail_module.Mail')
    def test_init_app(self, mock_mail):
        self.mail_sender.init_app(self.app)
        self.assertTrue(self.mail_sender.mail is not None)
        mock_mail.assert_called_once_with(self.app)

    @patch('your_mail_module.URLSafeTimedSerializer')
    def test_generate_confirmation_token(self, mock_serializer):
        mock_serializer.return_value.dumps.return_value = 'mock_token'
        email = 'test@example.com'
        sid = '12345'
        token = self.mail_sender.generate_confirmation_token(email, sid)
        self.assertEqual(token, 'mock_token')
        mock_serializer.return_value.dumps.assert_called_once()

    @patch('your_mail_module.URLSafeTimedSerializer')
    def test_confirm_token(self, mock_serializer):
        mock_serializer.return_value.loads.return_value = {'email': 'test@example.com', 'sid': '12345'}
        token = 'some_random_token'
        data = self.mail_sender.confirm_token(token)
        self.assertEqual(data, {'email': 'test@example.com', 'sid': '12345'})

    @patch('your_mail_module.URLSafeTimedSerializer')
    def test_confirm_token_expired(self, mock_serializer):
        mock_serializer.return_value.loads.side_effect = Exception('Token expired')
        token = 'expired_token'
        data = self.mail_sender.confirm_token(token)
        self.assertFalse(data)

    @patch('your_mail_module.Message')
    @patch('your_mail_module.Mail')
    def test_send_email(self, mock_mail, mock_message):
        self.mail_sender.mail = Mock()
        recipient = 'user@example.com'
        sid = 'user123'
        self.mail_sender.send_email(recipient, sid)
        self.mail_sender.mail.send.assert_called_once()
        args, kwargs = mock_message.call_args
        self.assertIn(recipient, kwargs['recipients'])

    def test_request_new_user(self):
        with patch.object(self.mail_sender, 'send_email') as mock_send_email:
            recipient = 'newuser@example.com'
            form_data = {'user_data': 'data'}
            self.mail_sender.request_new_user(recipient, form_data)
            mock_send_email.assert_called_once()

    def test_send_new_user_request_email(self):
        with patch.object(self.mail_sender, 'send_email') as mock_send_email:
            recipient = 'newrequest@example.com'
            form_data = {'sid': '123'}
            self.mail_sender.send_new_user_request_email(recipient, form_data)
            mock_send_email.assert_called_once()

    @patch('your_application.MailSender.send_email')
    def test_send_new_user_request(self, mock_send_email):
        mock_send_email.return_value = True

        with self.app.app_context():
            result = self.mail_sender.send_new_user_request(
                'admin@example.com',
                'http://example.com/validate?token=123',
                'New User Request'
            )

        mock_send_email.assert_called_once()

        self.assertTrue(result)

    @patch('your_application.MailSender.send_email')
    def test_send_new_user_request_failure(self, mock_send_email):
        mock_send_email.side_effect = Exception('Failed to send')

        with self.app.app_context():
            with self.assertRaises(Exception):
                self.mail_sender.send_new_user_request(
                    'admin@example.com',
                    'http://example.com/validate?token=123',
                    'New User Request'
                )

        mock_send_email.assert_called_once()

if __name__ == '__main__':
    unittest.main()
