from WEBSITE import create_flask_app
from flask import session

flask_app = create_flask_app()

if __name__ == '__main__':
    flask_app.run(debug=True)