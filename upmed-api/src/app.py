from .util.env import Env
from flask import Flask

from .api import api_endpoints
from flask_cors import CORS

"""
Create app and register blueprints

---Heroku Imports---
import os

from util.env import Env
from flask import Flask
from flask_cors import CORS

from api import api_endpoints


----Relative Imports----
from .util.env import Env
from flask import Flask

from .api import api_endpoints
from flask_cors import CORS


"""
app = Flask(__name__)
CORS(app)
api_endpoints.bind_to_app(app)


@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)


if __name__ == "__main__":
    app.run(port=Env.PORT())
