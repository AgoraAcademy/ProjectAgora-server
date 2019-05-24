import connexion
import six
import os
import requests
from flask import Flask, send_from_directory

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util, orm


def miniprogram_qr_get(qrtype):  # noqa: E501
    if qrtype == "dMGsnKEKLe.txt":
        return send_from_directory(os.path.dirname(os.environ["MINIPROGRAM_QR_VERIFICATION_FILE"]), 'dMGsnKEKLe.txt')
