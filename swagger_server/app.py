#!/usr/bin/env python3
# Dupilicate of __main__.py for heroku to operate
import connexion
import logging
from flask_cors import CORS
from swagger_server import encoder


app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
CORS(app.app, expose_headers=["Authorization", "refresh_token"])
app.add_api('swagger.yaml', arguments={'title': 'ProjectAgora'})
if __name__ == '__main__':
    app.run(port=8080)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
