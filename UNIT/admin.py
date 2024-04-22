import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  
from unittest.mock import patch
from flask import url_for
from WEBSITE import create_flask_app

class AdminRoutesTestCase(unittest.TestCase):
    """
    Testovací třída pro administrační cesty Flask web aplikace. Kontroluje správnost
    administrátorských funkcí, jako je správa uživatelů.
    """
    def setUp(self):
        """Inicializuje testovací klienta a nastavuje kontext aplikace."""
        self.app = create_flask_app()  
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Vymaze kontext aplikace po každém testu."""
        self.app_context.pop()

    def test_add_user_empty_fields(self):
        """Testuje, zda se správně zobrazí chybové zprávy při prázdných polích."""
        response = self.client.post('/admin/utilities/add_user', data={
            'user_first_name': '',
            'user_last_name': '',
            'user_email': '',
            'user_role': '',
            'BCN': '',
            'user_sid': '',
            'user_password': '',
            'confirm_password': ''
        })
        error_messages = [
            'Jméno musí obsahovat pouze písmena a mezery.',
            'Příjmení musí obsahovat pouze písmena a mezery.',
            'Email není ve správném formátu.',
            'BCN musí být deseticiferné číslo.',
            'SID musí být pěticiferné číslo.',
            'Heslo je krátké.'
        ]
        data = response.get_data(as_text=True)
        for message in error_messages:
            self.assertIn(message, data)
        self.assertEqual(response.status_code, 200)

    def test_add_user_invalid_email(self):
        """Testuje správnou chybovou zprávu při špatném emailovém formátu."""
        response = self.client.post('/admin/utilities/add_user', data={
            'user_first_name': 'John',
            'user_last_name': 'Doe',
            'user_email': 'bademail',
            'user_role': 'admin',
            'BCN': '1234567890',
            'user_sid': '12345',
            'user_password': 'Password1!',
            'confirm_password': 'Password1!'
        })
        self.assertIn('Email není ve správném formátu.', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_add_user_weak_password(self):
        """Testuje chybovou zprávu při zadání slabého hesla."""
        response = self.client.post('/admin/utilities/add_user', data={
            'user_first_name': 'Jane',
            'user_last_name': 'Doe',
            'user_email': 'jane@example.com',
            'user_role': 'admin',
            'BCN': '1234567890',
            'user_sid': '12345',
            'user_password': 'weak',
            'confirm_password': 'weak'
        })
        self.assertIn('Heslo je krátké.', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_add_user_passwords_do_not_match(self):
        """Testuje chybovou zprávu při neshodě zadaných hesel."""
        response = self.client.post('/admin/utilities/add_user', data={
            'user_first_name': 'John',
            'user_last_name': 'Smith',
            'user_email': 'john@example.com',
            'user_role': 'admin',
            'BCN': '1234567890',
            'user_sid': '54321',
            'user_password': 'Password1!',
            'confirm_password': 'Password2!'
        })
        self.assertIn('Hesla se neshodují.', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

































    def test_add_user_invalid_email(self):
        """aaaaa"""
        response = self.client.post('/admin/utilities/add_user', data={
            'user_first_name': 'John',
            'user_last_name': 'Doe',
            'user_email': 'bademail',
            'user_role': 'admin',
            'BCN': '1234567890',
            'user_sid': '12345',
            'user_password': 'Password1!',
            'confirm_password': 'Password1!'
        })
        self.assertIn('Email není ve správném formátu.', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_add_user_weak_password(self):
        """aaaaa"""
        response = self.client.post('/admin/utilities/add_user', data={
            'user_first_name': 'Jane',
            'user_last_name': 'Doe',
            'user_email': 'jane@example.com',
            'user_role': 'admin',
            'BCN': '1234567890',
            'user_sid': '12345',
            'user_password': 'weak',
            'confirm_password': 'weak'
        })
        self.assertIn('Heslo je krátké.', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    def test_add_user_passwords_do_not_match(self):
        """aaaaa"""
        response = self.client.post('/admin/utilities/add_user', data={
            'user_first_name': 'John',
            'user_last_name': 'Smith',
            'user_email': 'john@example.com',
            'user_role': 'admin',
            'BCN': '1234567890',
            'user_sid': '54321',
            'user_password': 'Password1!',
            'confirm_password': 'Password2!'
        })
        self.assertIn('Hesla se neshodují.', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    @patch('yourapplication.admin_routes.current_app.mysql.connection.cursor')
    def test_add_user_duplicate_email(self, mock_cursor):
        """aaaaa"""
        mock_cursor().fetchone.return_value = [1] 
        response = self.client.post('/admin/utilities/add_user', data={
            'user_first_name': 'John',
            'user_last_name': 'Doe',
            'user_email': 'john@example.com',
            'user_role': 'admin',
            'BCN': '1234567890',
            'user_sid': '12345',
            'user_password': 'Password1!',
            'confirm_password': 'Password1!'
        })
        self.assertIn('Uživatel s tímto emailem již existuje.', response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)

    @patch('yourapplication.admin_routes.current_app.mysql.connection.cursor')
    def test_add_user_successful_creation(self, mock_cursor):

        mock_cursor().fetchone.side_effect = [None, None]  
        mock_cursor().execute.return_value = None
        mock_cursor().close.return_value = None
        response = self.client.post('/admin/utilities/add_user', data={
            'user_first_name': 'Jane',
            'user_last_name': 'Smith',
            'user_email': 'jane@example.com',
            'user_role': 'manager',
            'BCN': '0987654321',
            'user_sid': '67890',
            'user_password': 'Password1!',
            'confirm_password': 'Password1!'
        }, follow_redirects=True)
        self.assertIn('route for successful creation', response.get_data(as_text=True))  
        self.assertEqual(response.status_code, 200)
    
    @patch('WEBSITE.admin_routes.URLSafeTimedSerializer')
    def test_request_add_user_success(self, mock_serializer):  

        expected_user_details = {'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'}
        mock_serializer.return_value.loads.return_value = expected_user_details
        
        with self.app.test_request_context():
            response = self.client.get(url_for('admin_routes.request_add_user', token='valid-token'))
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue('user_details' in response.context)
            self.assertDictEqual(response.context['user_details'], expected_user_details)

    @patch('WEBSITE.admin_routes.URLSafeTimedSerializer')
    def test_request_add_user_invalid_token(self, mock_serializer):

        mock_serializer.return_value.loads.side_effect = Exception("Invalid Token")
        
        with self.app.test_request_context(), self.client as c:
            response = c.get(url_for('admin_routes.request_add_user', token='invalid-token'), follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue('The registration link is invalid or has expired.' in response.get_data(as_text=True))        
    
    def test_submit_new_user_get(self):

        response = self.client.get(url_for('admin_routes.submit_new_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('admin/add_user.html')

    def test_submit_new_user_post_success(self):

        with patch('WEBSITE.admin_routes.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.execute.return_value = True
            response = self.client.post(url_for('admin_routes.submit_new_user'), data={
                'user_first_name': 'Test',
                'user_last_name': 'User',
                'user_email': 'test@example.com',
                'user_role': 'admin',
                'BCN': '1234567890',
                'SID': '54321',
                'user_password': 'Password@1',
                'confirm_password': 'Password@1'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('New user has been successfully created.', response.get_data(as_text=True))

    def test_submit_new_user_post_validation_errors(self):

        response = self.client.post(url_for('admin_routes.submit_new_user'), data={
            'user_first_name': '',  
            'user_last_name': '', 
            'user_email': 'invalidemail',  
            'user_role': 'nonexistentrole',  
            'BCN': '123',  
            'SID': 'abcde',  
            'user_password': 'pass',
            'confirm_password': 'password' 
        })
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        self.assertIn('First name is required.', data)
        self.assertIn('Last name is required.', data)
        self.assertIn('Email is not in the correct format.', data)
        self.assertIn('Role is not valid.', data)
        self.assertIn('BCN must be a 10-digit number.', data)
        self.assertIn('SID must be a 5-digit number.', data)
        self.assertIn('Passwords do not match.', data)

    def test_submit_new_user_post_db_error(self):

        with patch('WEBSITE.admin_routes.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.execute.side_effect = Exception('Database error')
            response = self.client.post(url_for('admin_routes.submit_new_user'), data={
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Error adding new user:', response.get_data(as_text=True))

    def test_manage_users(self):

        response = self.client.get(url_for('admin_routes.manage_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('admin/manage_users.html')

    @patch('WEBSITE.admin_routes.current_app.mysql.connection.cursor')
    def test_get_all_employees(self, mock_cursor):
        mock_employees = [
            ('123', 'John', 'Doe', 'john@example.com', '1234567890', 'admin'),
        ]
        mock_cursor.return_value.fetchall.return_value = mock_employees

        response = self.client.get(url_for('admin_routes.get_all_employees'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {'user_sid': '123', 'first_name': 'John', 'last_name': 'Doe', 'user_email': 'john@example.com', 'bcn': '1234567890', 'user_role': 'admin'},
        ])

    @patch('WEBSITE.admin_routes.current_app.mysql.connection.cursor')
    def test_search_users_with_query(self, mock_cursor):

        mock_filtered_users = [
        ]
        mock_cursor.return_value.fetchall.return_value = mock_filtered_users

        response = self.client.get(url_for('admin_routes.search_users', query='John'))
        self.assertEqual(response.status_code, 200)

    def test_search_users_empty_query(self):

        response = self.client.get(url_for('admin_routes.search_users'))
        self.assertEqual(response.status_code, 200)

    @patch('WEBSITE.admin_routes.current_app.mysql.connection.cursor')
    def test_delete_user_success(self, mock_cursor):

        mock_cursor.return_value.fetchone.return_value = ['John', 'Doe']

        with patch('WEBSITE.admin_routes.deletion_logger') as mock_logger:
            response = self.client.delete(url_for('admin_routes.delete_user', user_sid=123), json={'reason': 'No longer employed'})
            self.assertEqual(response.status_code, 200)
            mock_logger.info.assert_called_once()

    @patch('WEBSITE.admin_routes.current_app.mysql.connection.cursor')
    def test_delete_user_not_found(self, mock_cursor):

        mock_cursor.return_value.fetchone.return_value = None

        response = self.client.delete(url_for('admin_routes.delete_user', user_sid=999))
        self.assertEqual(response.status_code, 404)

    @patch('WEBSITE.admin_routes.current_app.mysql.connection.cursor')
    def test_delete_user_db_error(self, mock_cursor):

        mock_cursor.return_value.fetchone.return_value = ['John', 'Doe']
        mock_cursor.return_value.execute.side_effect = Exception('Database error')

        with patch('WEBSITE.admin_routes.deletion_logger') as mock_logger:
            response = self.client.delete(url_for('admin_routes.delete_user', user_sid=123), json={'reason': 'No longer employed'})
            self.assertEqual(response.status_code, 500)
            mock_logger.error.assert_called_once()