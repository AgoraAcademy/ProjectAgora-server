#!/usr/bin/env python3

import connexion
from flask_cors import CORS
from swagger_server import encoder
from flask_sqlalchemy import SQLAlchemy
import os


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    CORS(app.app)
    app.add_api('swagger.yaml', arguments={'title': 'ProjectAgora'})
    db = SQLAlchemy(app)
    app.run(port=8080)


if __name__ == '__main__':
    main()
