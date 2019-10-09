from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from app.main.controller import api
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_pyfile('app\config.cfg')

api.init_app(app)
app.run(debug=True,host="0.0.0.0") 