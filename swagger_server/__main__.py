#!/usr/bin/env python3

import connexion
from flask_cors import CORS
from swagger_server import encoder
import os


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    CORS(app.app)
    app.add_api('swagger.yaml', arguments={'title': 'ProjectAgora'})
    try:
        app.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
    except Exception as e:
        return {"error": e, "message": "failed to initialize sqlalchemy db."}
    app.run(port=8080)


if __name__ == '__main__':
    main()
