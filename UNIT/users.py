import unittest
from unittest.mock import patch
from flask import Flask, url_for
from WEBSITE import user_routes  
from werkzeug.exceptions import BadRequestKeyError

class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.app.register_blueprint(user_routes)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_change_my_informations_without_sid(self):
        with self.client as client:
            response = client.get('/user/change_my_informations', follow_redirects=True)
            self.assertIn('Přihlášení vypršelo, přihlašte se znovu.', response.get_data(as_text=True))
            self.assertTrue('/login', url_for('authentication_routes.login') in response.headers['Location'])

    def test_change_my_informations_user_not_found(self):
        with self.client as client, patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.execute.return_value = None
            mock_cursor.return_value.fetchone.return_value = None
            response = client.get('/user/change_my_informations', follow_redirects=True)
            self.assertIn('Nepodařilo se načíst data uživatele.', response.get_data(as_text=True))
            self.assertTrue('/login', url_for('authentication_routes.login') in response.headers['Location'])

    def test_change_my_informations_database_error(self):
        with self.client as client, patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.side_effect = Exception('Database error')
            response = client.get('/user/change_my_informations')
            self.assertEqual(response.status_code, 500)
            self.assertIn('Database error', response.get_data(as_text=True))

    def test_update_information_without_sid(self):
        response = self.client.post('/user/update_information', follow_redirects=True)
        self.assertIn('Přihlášení vypršelo, přihlašte se znovu.', response.get_data(as_text=True))
        self.assertTrue('/login', url_for('authentication_routes.login') in response.headers['Location'])

    def test_update_information_invalid_email_format(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            response = client.post('/user/update_information', data={
                'user_email': 'bademail', 'user_school_email': 'stillbademail'
            }, follow_redirects=True)
            self.assertIn('Jeden nebo oba emaily nejsou ve správném formátu.', response.get_data(as_text=True))

    def test_update_information_duplicate_email(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.execute.side_effect = [None, [(1,)]]
                response = client.post('/user/update_information', data={
                    'user_email': 'test@example.com',
                    'user_school_email': 'school@example.com'
                }, follow_redirects=True)
                self.assertIn('Email is already in use.', response.get_data(as_text=True))

    def test_update_information_data_validation_error(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            response = client.post('/user/update_information', data={
                'user_email': 'invalid_email',
            }, follow_redirects=True)
            self.assertIn('Invalid email format.', response.get_data(as_text=True))

    def test_update_information_database_update_error(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.execute.side_effect = Exception('Database update error')
                response = client.post('/user/update_information', follow_redirects=True)
                self.assertIn('Database update error', response.get_data(as_text=True))

    def test_update_information_missing_required_fields(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            response = client.post('/user/update_information', data={}, follow_redirects=True)
            self.assertIn('Missing required information', response.get_data(as_text=True))

    def test_add_user_without_sid(self):
        response = self.client.get('/home_boss/add_user', follow_redirects=True)
        self.assertIn('Přihlášení vypršelo, přihlašte se znovu.', response.get_data(as_text=True))
        self.assertTrue('/login', url_for('authentication_routes.login') in response.headers['Location'])

    def test_add_user_duplicate_user_check(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.execute.side_effect = [None, [(1,)]]
                response = client.post('/home_boss/add_user', data={
                    'user_email': 'duplicate@example.com'
                }, follow_redirects=True)
                self.assertIn('User already exists.', response.get_data(as_text=True))

    def test_add_user_form_incomplete_data(self):
            with self.client as client:
                with client.session_transaction() as sess:
                    sess['user_info'] = {'sid': 'valid_sid'}
                response = client.post('/home_boss/add_user', data={
                    'user_first_name': 'John',
                    'user_last_name': 'Doe'
                }, follow_redirects=True)
                self.assertIn('Some required information is missing.', response.get_data(as_text=True))

    def test_add_user_database_insertion_error(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.execute.side_effect = Exception("Insertion failed")
                response = client.post('/home_boss/add_user', data={
                    'user_first_name': 'John',
                    'user_last_name': 'Doe',
                    'user_email': 'john@example.com'
                }, follow_redirects=True)
                self.assertIn('Failed to add new user due to a database error.', response.get_data(as_text=True))

    def test_add_user_bad_request_key_error(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_info'] = {'sid': 'valid_sid'}
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.side_effect = BadRequestKeyError('Missing key')
                response = client.post('/home_boss/add_user', follow_redirects=True)
                self.assertIn('Missing required form data.', response.get_data(as_text=True))

    def test_general_database_connection_error(self):
        with self.client as client:
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.side_effect = Exception("Database connection failed")
                response = client.get('/home_boss/add_user', follow_redirects=True)
                self.assertIn('Database connection error occurred.', response.get_data(as_text=True))

    def test_general_unexpected_error_handling(self):
        with self.client as client:
            with patch('your_flask_app.user_routes.change_my_informations') as mock_route:
                mock_route.side_effect = Exception("Unexpected error")
                response = client.get('/user/change_my_informations', follow_redirects=True)
                self.assertIn('An unexpected error occurred.', response.get_data(as_text=True))

    def test_general_user_session_timeout_handling(self):
        with self.client as client:
            response = client.get('/user/update_information', follow_redirects=True)
            self.assertIn('Your session has expired, please log in again.', response.get_data(as_text=True))
            self.assertTrue('/login', url_for('authentication_routes.login') in response.headers['Location'])
     

        if __name__ == '__main__':
            unittest.main()