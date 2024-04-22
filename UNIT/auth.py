import unittest
import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
from unittest.mock import patch
from flask import Flask, session, template_rendered
from contextlib import contextmanager
from WEBSITE import authentication_routes 

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

class AuthenticationRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        self.app.register_blueprint(authentication_routes)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()

    def test_login_get_route_renders_template(self):
        with captured_templates(self.app) as templates:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(templates[0][0].name, 'login/login.html')

    def test_login_post_with_valid_credentials(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor, \
             patch('werkzeug.security.check_password_hash') as mock_check_password:
            mock_cursor.return_value.fetchone.return_value = ('valid_hashed_password', 'Admin')
            mock_check_password.return_value = True

            response = self.client.post('/', data={'sid': 'valid_sid', 'password': 'correct_password'}, follow_redirects=True)
            self.assertEqual(session.get('user_info')['role'], 'Admin')
            self.assertEqual(response.status_code, 200)

    def test_login_post_with_incorrect_password(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor, \
             patch('werkzeug.security.check_password_hash') as mock_check_password:
            mock_cursor.return_value.fetchone.return_value = ('valid_hashed_password', 'Admin')
            mock_check_password.return_value = False

            response = self.client.post('/', data={'sid': 'valid_sid', 'password': 'wrong_password'})
            self.assertIn('Nesprávné heslo.', response.get_data(as_text=True))
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(session.get('user_info'))

    def test_login_post_with_non_existent_user(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.fetchone.return_value = None  

            response = self.client.post('/', data={'sid': 'invalid_sid', 'password': 'any_password'})
            self.assertIn('Nesprávné SID.', response.get_data(as_text=True))
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(session.get('user_info'))

    def test_login_post_with_unrecognized_role(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor, \
             patch('werkzeug.security.check_password_hash') as mock_check_password:
            mock_cursor.return_value.fetchone.return_value = ('valid_hashed_password', 'UnknownRole')
            mock_check_password.return_value = True

            response = self.client.post('/', data={'sid': 'valid_sid', 'password': 'correct_password'})
            self.assertIn('Role nebyla rozpoznána.', response.get_data(as_text=True))
            self.assertEqual(response.status_code, 200)

    def test_login_post_redirects_if_already_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_info'] = {'role': 'Admin', 'sid': 'valid_sid'}
            
            response = c.post('/', data={'sid': 'valid_sid', 'password': 'correct_password'}, follow_redirects=True)
            self.assertNotIn('login.html', response.get_data(as_text=True))

    def test_manage_profile_redirects_when_not_logged_in(self):
        response = self.client.get('/user/manage_profile')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login' in response.headers['Location'])

    def test_manage_profile_loads_correct_data(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.fetchone.return_value = (
                    'valid_sid', 'path/to/pic.jpg', 'John', 'Doe', 'Dr.', 'PhD', '1234567890',
                    'john@example.com', '123-456-7890', '123 Main St', 'Admin', 'john@school.com',
                    '321-654-9870', 'Springfield Elementary'
                )
                response = c.get('/user/manage_profile')
                self.assertEqual(response.status_code, 200)
                self.assertIn('John Doe', response.get_data(as_text=True))

    def test_manage_profile_handles_nonexistent_sid(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_info'] = {'sid': 'nonexistent_sid'}

            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.fetchone.return_value = None  
                response = c.get('/user/manage_profile', follow_redirects=True)
                self.assertIn('No user data found for the provided SID.', response.get_data(as_text=True))
                self.assertTrue('/login' in response.headers['Location'])

    def test_load_user_data_without_sid(self):
        with self.client as c:
            response = c.get('/get_user_data')
            self.assertEqual(response.status_code, 400)
            self.assertIn('No SID provided.', response.get_data(as_text=True))

    def test_load_user_data_with_valid_sid(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.fetchone.return_value = ('John', 'Doe', 'Admin')
                response = c.get('/get_user_data')
                self.assertEqual(response.status_code, 200)
                self.assertIn('John Doe', response.get_data(as_text=True))

    def test_load_user_data_with_invalid_sid(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_info'] = {'sid': 'invalid_sid'}

            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.fetchone.return_value = None  
                response = c.get('/get_user_data')
                self.assertEqual(response.status_code, 404)
                self.assertIn('User data not found.', response.get_data(as_text=True))

    def test_logout_clears_session_and_redirects(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid', 'role': 'Admin'}
            
            response = c.get('/logout', follow_redirects=True)
            self.assertIsNone(session.get('user_info'))
            self.assertTrue('/login' in response.headers['Location'])

    def test_login_post_with_duplicate_sids(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.fetchone.side_effect = [('hashed_password', 'Admin'), ('hashed_password', 'Admin')]
            response = self.client.post('/', data={'sid': 'duplicate_sid', 'password': 'correct_password'})
            self.assertIn('Multiple accounts found for SID.', response.get_data(as_text=True))
            self.assertEqual(response.status_code, 200)

    def test_login_post_with_db_connection_error(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.side_effect = Exception("Database connection error")
            response = self.client.post('/', data={'sid': 'any_sid', 'password': 'any_password'})
            self.assertIn('Database connection error', response.get_data(as_text=True))
            self.assertEqual(response.status_code, 500)

    def test_manage_profile_with_db_connection_error(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.side_effect = Exception("Database connection error")
                response = c.get('/user/manage_profile')
                self.assertIn('Database connection error', response.get_data(as_text=True))
                self.assertEqual(response.status_code, 500)

    def test_load_user_data_with_db_connection_error(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.side_effect = Exception("Database connection error")
                response = c.get('/get_user_data')
                self.assertIn('Database connection error', response.get_data(as_text=True))
                self.assertEqual(response.status_code, 500)

    def test_logout_post_route(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_info'] = {'role': 'Admin', 'sid': 'valid_sid'}
            response = c.post('/logout', follow_redirects=True)
            self.assertIsNone(session.get('user_info'))
            self.assertTrue('/login' in response.headers['Location'])

if __name__ == '__main__':
    unittest.main()