from flask import Flask
from views import report_api

server = Flask(__name__)
server.register_blueprint(report_api.blueprint)

if __name__ == "__main__":
    # Run the Flask app with Celery
    server.run()