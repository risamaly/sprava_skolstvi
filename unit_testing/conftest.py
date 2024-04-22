import pytest
"""from WEBSITE import create_flask_app
from DATABASE import Database_Config"""
from WEBSITE import routes, admin_routes, authentication_routes, create_flask_app
from DATABASE.database_config import Database_Config


@pytest.fixture()
def app():
    app = create_flask_app("sqlite://")

    with app.app_context():
        Database_Config.test_connections()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

