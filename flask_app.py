import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),".."))
from WEBSITE import create_flask_app
from flask import session

flask_app = create_flask_app()

if __name__ == '__main__':
    flask_app.run(debug=True)