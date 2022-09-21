"""Flask app for starting server."""
from flasgger import Swagger, swag_from
from flask import Flask, jsonify, redirect, render_template, request
from flask_httpauth import HTTPBasicAuth
import os


auth = HTTPBasicAuth()
app = Flask(__name__)
app.config["SWAGGER"] = {
    "uiversion": 3,
    "swagger": "2.0",
    "info": {
        "title": "Rule Engine",
        "description": "Rule Engine API",
        "contact": {
            "responsibleOrganization": "Me",
            "responsibleDeveloper": "Joao Almeida",
        },
        "termsOfService": "http://me.com/terms",
        "version": "0.0.1",
    },
    # "host": "http://bibliovigilancia.gim.med.up.pt/",  # overrides localhost:5000
    "basePath": "api",  # base bash for blueprint registration
    "schemes": ["http", "https"],
}
swagger = Swagger(app, template=app.config["SWAGGER"])


import engine_api.views
