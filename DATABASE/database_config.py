import mysql.connector
from mysql.connector import Error
from LOG.logging import setup_logger

class Database_Config:
    """Configurace Databaze"""
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DATABASE = 'sprava_skolstvi_database'

    logger = setup_logger('database_logger')

    def test_connections(self):
        """Testuje připojení do databaze"""
        is_connected = False
        try:
            database_connection = mysql.connector.connect(
                host=self.MYSQL_HOST,
                user=self.MYSQL_USER,
                password=self.MYSQL_PASSWORD,
                database=self.MYSQL_DATABASE
            )
            if database_connection.is_connected():
                self.logger.info("Susscefuly connected.")
                database_connection.close()
                is_connected = True
        except Error as e:
            self.logger.error(f"Error while connecting {e}")
        return is_connected
    