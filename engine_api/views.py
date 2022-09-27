from flasgger import swag_from, validate
from flask import jsonify, redirect, render_template, request, session
import pandas as pd
from engine_api.rule_engine import apply_rules, read_rules_from_csv, create_decision
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


@app.route("/api/v1/<rule_nr>", methods=["POST"])
@auth.login_required
def apply_rule0(rule_nr):
    data = request.json
    validate(
        data,
        "input",
        os.path.join(path, "engine_api", "docs", rule_nr + ".yml"),
    )
    if rule_nr in rules.keys():

        decision, decision_path = create_decision(data, rules[rule_nr])
    else:
        return {"message": "Invalid rule number"}
    return jsonify(
        {
            "decision": decision,
            "decision_path": ",".join([str(x) for x in decision_path]),
        }
    )
