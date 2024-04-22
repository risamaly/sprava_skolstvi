import unittest
import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
from unittest.mock import patch
from flask import Flask, url_for
from WEBSITE import student_routes  

class TestStudentRoutes(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'super_secret_key'
        self.app.register_blueprint(student_routes)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_student_profile_success(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.execute.return_value = None
            mock_cursor.return_value.fetchone.return_value = (1, 'path/to/image.jpg', 'John', 'Doe', '123456789', 'john.doe@example.com', '123-456-7890', '123 Main St', 'parent@example.com', '321-654-9870', '321 Side St')
            mock_cursor.return_value.description = [('student_id',), ('user_profile_pic',), ('first_name',), ('last_name',), ('bcn',), ('student_email',), ('student_phone_number',), ('student_adress',), ('parent_email',), ('parent_phone_number',), ('parent_adress',)]
            response = self.client.get('/student_profile/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn('John Doe', response.get_data(as_text=True))

    def test_student_profile_not_found(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.return_value.execute.return_value = None
            mock_cursor.return_value.fetchone.return_value = None
            response = self.client.get('/student_profile/999', follow_redirects=True)
            self.assertIn('Student nebyl nalezen.', response.get_data(as_text=True))
            self.assertTrue('home_teacher', url_for('routes.home_teacher') in response.headers['Location'])

    def test_student_profile_database_error(self):
        with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
            mock_cursor.side_effect = Exception("Database error")
            response = self.client.get('/student_profile/1')
            self.assertEqual(response.status_code, 500)
            self.assertIn('Database error', response.get_data(as_text=True))

    def test_student_profile_access_control(self):
        with self.client as client:
            response = client.get('/student_profile/1')
            self.assertNotEqual(response.status_code, 200) 
            self.assertIn('Please log in to access this page.', response.get_data(as_text=True))

    def test_student_profile_sql_injection(self):
        with self.client as client:
            with patch('flask.current_app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.execute.return_value = None
                mock_cursor.return_value.fetchone.return_value = None
                response = client.get('/student_profile/1 OR 1=1')
                mock_cursor.return_value.execute.assert_called_with(
                    "SELECT student_id, user_profile_pic, first_name, last_name, bcn, student_email, "
                    "student_phone_number, student_adress, parent_email, parent_phone_number, parent_adress "
                    "FROM students WHERE student_id = %s", ('1 OR 1=1',)
                )
                self.assertNotEqual(response.status_code, 200) 


if __name__ == '__main__':
    unittest.main()
