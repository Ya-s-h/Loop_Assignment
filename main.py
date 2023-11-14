from flask import Flask
from views import report_api
server = Flask(__name__)

server.register_blueprint(report_api.blueprint)
server.run()
