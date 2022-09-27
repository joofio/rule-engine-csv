"""Flask app for starting server."""
from flasgger import Swagger, swag_from
from flask import Flask, jsonify, redirect, render_template, request
from flask_httpauth import HTTPBasicAuth
import os
import config

auth = HTTPBasicAuth()
app = Flask(__name__)

swagger = Swagger(app, template=config.SWAGGER_TEMPLATE)


import engine_api.views
