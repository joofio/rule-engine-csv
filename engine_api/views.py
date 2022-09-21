from flasgger import swag_from
from flask import jsonify, redirect, render_template, request, session
import pandas as pd
from engine_api.rule_engine import apply_rules, read_rules_from_csv, create_decision
from engine_api import app, auth

rule0 = read_rules_from_csv("rules.csv")
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
@auth.login_required
# @swag_from("docs/logsearch.yml", validation=True)  # validates data automatically
def apply_rule0():
    data = request.json["data"]
    # print(data)
    # print(rule0)
    decision, decision_path = create_decision(data, rule0)
    return jsonify(
        {
            "decision": decision,
            "decision_path": ",".join([str(x) for x in decision_path]),
        }
    )
