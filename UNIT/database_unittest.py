from binascii import Error
import unittest
from unittest.mock import patch, MagicMock
from DATABASE.database_config import Database_Config

class TestDatabaseConfig(unittest.TestCase):
   
    def setUp(self):
        self.db_config = Database_Config()

    @patch('current_app.mysql.connector.connect')
    @patch('LOG.logging.setup_logger')
    def test_successful_connection(self, mock_setup_logger, mock_connect):
        mock_logger = MagicMock()
        mock_setup_logger.return_value = mock_logger

        mock_connection = MagicMock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection

        self.assertTrue(self.db_config.test_connections())
        mock_logger.info.assert_called_once_with("Připojení k databázi bylo úspěšné.")
        mock_connection.close.assert_called_once()

    
    def test_failed_connection(self, mock_setup_logger, mock_connect):
        mock_logger = MagicMock()
        mock_setup_logger.return_value = mock_logger
        
        mock_connect.side_effect = Error("Failed to connect")

        self.assertFalse(self.db_config.test_connections())
        mock_logger.error.assert_called_once_with("Chyba při připojování k databázi: Failed to connect")

if __name__ == '__main__':
    unittest.main()
