import unittest
import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
from unittest.mock import patch
from flask import Flask, url_for, template_rendered
from contextlib import contextmanager
from WEBSITE import routes, admin_routes, authentication_routes 

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'jecna'
        self.app.register_blueprint(routes)
        self.app.register_blueprint(admin_routes)
        self.app.register_blueprint(authentication_routes)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_admin_route_access(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'role': 'Admin'}
            response = client.get('/admin')
            self.assertEqual(response.status_code, 200)
            self.assertIn('admin/admin_home.html', response.get_data(as_text=True))

    def test_admin_access_without_login(self):
        response = self.client.get('/admin', follow_redirects=True)
        self.assertIn('login', response.request.path)
        self.assertNotIn('admin/admin_home.html', response.get_data(as_text=True))
    
    def test_boss_route_access(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}  
            response = client.get('/home_boss')
            self.assertEqual(response.status_code, 200)
            self.assertIn('user/boss.html', response.get_data(as_text=True))

    def test_boss_access_without_login(self):
        response = self.client.get('/home_boss', follow_redirects=True)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login', url_for('authentication_routes.login') in response.headers['Location'])

    def test_boss_with_invalid_user_sid(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'invalid_sid'}
            response = client.get('/home_boss')
            self.assertNotIn('Škola nenalezena', response.get_data(as_text=True))
            self.assertIn('Přihlášení vypršelo, přihlašte se znovu.', response.get_data(as_text=True))

    def test_boss_with_no_school_assigned(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_but_unassigned_sid'}
            response = client.get('/home_boss')
            self.assertIn('Škola nenalezena', response.get_data(as_text=True))
            self.assertNotIn('employees', response.get_data(as_text=True))

    def test_deputy_route_access(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'role': 'Deputy'}
            response = client.get('/home_deputy')
            self.assertEqual(response.status_code, 200)
            self.assertIn('user/deputy.html', response.get_data(as_text=True))

    def test_teacher_route_access(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'role': 'Teacher', 'sid': 'valid_teacher_sid'}
            response = client.get('/home_teacher')
            self.assertEqual(response.status_code, 200)
            self.assertIn('user/teacher.html', response.get_data(as_text=True))

    def test_teacher_access_without_login(self):
        response = self.client.get('/home_teacher', follow_redirects=True)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login', url_for('authentication_routes.login') in response.headers['Location'])

    def test_teacher_with_no_class_assigned(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'role': 'Teacher', 'sid': 'teacher_without_class'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.execute.return_value = None
                mock_cursor.return_value.fetchone.return_value = None
            response = client.get('/home_teacher')
            self.assertIn('Učitel nemá přiřazenou žádnou třídu.', response.get_data(as_text=True))
            self.assertNotIn('class_info', response.get_data(as_text=True))

    def test_get_all_students_without_login(self):
        response = self.client.get('/get_all_students')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Uživatel není přihlášen.', response.get_data(as_text=True))

    def test_get_all_students_with_valid_session(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'teacher_with_class'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.execute.return_value = None
                mock_cursor.return_value.fetchall.return_value = [
                    ('1', 'John', 'Doe', 'john.doe@example.com'),
                    ('2', 'Jane', 'Doe', 'jane.doe@example.com')
                ]
            response = client.get('/get_all_students')
            self.assertEqual(response.status_code, 200)
            self.assertIn('John Doe', response.get_data(as_text=True))
            self.assertIn('Jane Doe', response.get_data(as_text=True))

    def test_get_all_students_with_no_class_assigned(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'teacher_without_class'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.fetchone.return_value = None
            response = client.get('/get_all_students')
            self.assertEqual(response.status_code, 404)
            self.assertIn('Učitel nemá přiřazenou žádnou třídu.', response.get_data(as_text=True))

    def test_lost_password_route_get(self):
        response = self.client.get('/lost_password')
        self.assertEqual(response.status_code, 200)
        self.assertIn('login/lost_password.html', response.get_data(as_text=True))

    def test_lost_password_submit_valid_email(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.fetchone.return_value = ('valid_sid',)
            with patch('flask.current_app.mail_sender.send_email') as mock_send_email:
                response = self.client.post('/lost_password', data={'email': 'valid@example.com'}, follow_redirects=True)
                mock_send_email.assert_called_once_with('valid@example.com', 'valid_sid')
                self.assertIn('Email pro obnovu hesla byl odeslán.', response.get_data(as_text=True))

    def test_lost_password_submit_invalid_email(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.fetchone.return_value = None
            response = self.client.post('/lost_password', data={'email': 'invalid@example.com'})
            self.assertIn('Email není registrován v databázi.', response.get_data(as_text=True))

    def test_lost_password_email_send_failure(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.fetchone.return_value = ('valid_sid',)
            with patch('flask.current_app.mail_sender.send_email') as mock_send_email:
                mock_send_email.side_effect = Exception("Failed to send email")
                response = self.client.post('/lost_password', data={'email': 'valid@example.com'}, follow_redirects=True)
                self.assertIn('Chyba při odesílání emailu.', response.get_data(as_text=True))

    def test_password_reset_page_load(self):
        with self.client as client:
            with patch('your_flask_app.routes.current_app.mail_sender.confirm_token') as mock_confirm:
                mock_confirm.return_value = {'sid': '123', 'email': 'user@example.com'}
                response = client.get('/reset_password/some_valid_token')
                self.assertEqual(response.status_code, 200)
                self.assertIn('login/reset_password.html', response.get_data(as_text=True))

    def test_password_reset_with_invalid_token(self):
        with self.client as client:
            with patch('your_flask_app.routes.current_app.mail_sender.confirm_token') as mock_confirm:
                mock_confirm.return_value = False
                response = client.get('/reset_password/invalid_token', follow_redirects=True)
                self.assertIn('Odkaz pro obnovu hesla je neplatný nebo vypršel.', response.get_data(as_text=True))
                self.assertTrue('/login', url_for('authentication_routes.login') in response.headers['Location'])

    def test_password_reset_post_success(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': '123', 'email': 'user@example.com'}
            with patch('your_flask_app.routes.current_app.mail_sender.confirm_token') as mock_confirm:
                mock_confirm.return_value = {'sid': '123', 'email': 'user@example.com'}
                with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                    mock_cursor.return_value.execute.return_value = None
                    response = client.post('/reset_password/valid_token', data={
                        'password': 'ValidPassword1!',
                        'password2': 'ValidPassword1!'
                    }, follow_redirects=True)
                    self.assertIn('Vaše heslo bylo úspěšně změněno.', response.get_data(as_text=True))

    def test_password_reset_post_failure(self):
        with self.client as client:
            response = client.post('/reset_password/valid_token', data={
                'password': 'password',
                'password2': 'different_password'
            })
            self.assertIn('Hesla se neshodují.', response.get_data(as_text=True))

    def test_password_reset_post_with_inadequate_password(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': '123', 'email': 'user@example.com'}
            response = client.post('/reset_password/valid_token', data={
                'password': 'short',
                'password2': 'short'
            })
            self.assertIn('Heslo je příliš krátké.', response.get_data(as_text=True))
            self.assertIn('Heslo musí obsahovat alespoň jedno velké písmeno.', response.get_data(as_text=True))
            self.assertIn('Heslo musí obsahovat alespoň jedno číslo.', response.get_data(as_text=True))
            self.assertIn('Heslo musí obsahovat alespoň jeden speciální znak.', response.get_data(as_text=True))

    def test_password_reset_database_update_failure(self):
        with self.client as client:
            with patch('your_flask_app.routes.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.execute.side_effect = Exception("Database error")
                response = client.post('/reset_password/valid_token', data={
                    'password': 'ValidPassword1!',
                    'password2': 'ValidPassword1!'
                }, follow_redirects=True)
                self.assertIn('Chyba při změně hesla:', response.get_data(as_text=True))

    def test_database_connection_error_handling(self):
        with self.client as client:
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.side_effect = Exception("Database connection error")
                response = client.get('/some_route_that_queries_database')
                self.assertEqual(response.status_code, 500)
                self.assertIn('Database connection error', response.get_data(as_text=True))

    def test_unexpected_error_handling(self):
        with self.client as client:
            with patch('your_flask_app.routes.some_function') as mock_function:
                mock_function.side_effect = Exception("Unexpected error")
                response = client.get('/route_that_uses_some_function')
                self.assertEqual(response.status_code, 500)
                self.assertIn('Unexpected error', response.get_data(as_text=True))

    def test_user_session_timeout_handling(self):
        with self.client as client:
            response = client.get('/route_that_requires_login', follow_redirects=True)
            self.assertIn('Přihlášení vypršelo, přihlašte se znovu.', response.get_data(as_text=True))
            self.assertTrue('/login', url_for('authentication_routes.login') in response.headers['Location'])


    if __name__ == '__main__':
        unittest.main()
