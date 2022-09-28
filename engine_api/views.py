from flasgger import swag_from, validate
from flask import jsonify, redirect, render_template, request, session
import pandas as pd
from engine_api.rule_engine import (
    apply_rules,
    read_rules_from_csv,
    create_decision,
    routing,
)
from engine_api import app, auth
import re
import os
import glob


# use glob to get all the csv files
# in the folder
path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "engine_api", "algorithms", "*.csv"))
print(csv_files)
rules = {}
# loop over the list of csv files
for f in csv_files:
    df = read_rules_from_csv(f)
    rules[f.split("/")[-1].split(".")[0]] = df

print(rules)
# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
@auth.verify_password
def verify_password(username, password):
    if username != "admin" and password != "admin":
        return False
    return True


@app.route("/", methods=["GET"])
def search():
    return {"message": "Hello, World!"}


@app.route("/docs", methods=["GET"])
def redirection():
    return redirect("/apidocs")


@app.route("/api/v1/rule0", methods=["POST"])
@swag_from(
    os.path.join(path, "engine_api", "docs", "rule0.yml"),
    validation=True,
)
@auth.login_required
def apply_rule0():
    return routing(request, rules, "rule0")


# only separated because of the different yml file
@app.route("/api/v1/penicillin/intake_ge2h", methods=["POST"])
@swag_from(
    os.path.join(path, "engine_api", "docs", "penicillin_intake_ge2h.yml"),
    validation=True,
)
@auth.login_required
def apply_penicillin_intake_ge2h():
    return routing(request, rules, "penicillin_intake_ge2h")


@app.route("/api/v1/penicillin/intake_lt2h", methods=["POST"])
@swag_from(
    os.path.join(path, "engine_api", "docs", "penicillin_intake_lt2h.yml"),
    validation=True,
)
@auth.login_required
def apply_penicillin_intake_lt2h():
    return routing(request, rules, "penicillin_intake_lt2h")


@app.route("/api/v1/penicillin/intake_notknow", methods=["POST"])
@swag_from(
    os.path.join(path, "engine_api", "docs", "penicillin_intake_notknow.yml"),
    validation=True,
)
@auth.login_required
def apply_penicillin_intake_notknow():
    return routing(request, rules, "penicillin_intake_notknow")
