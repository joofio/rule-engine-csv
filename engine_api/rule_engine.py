#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from flask import jsonify, redirect, render_template, request, session


# read_rules
def read_rules_from_csv(path):
    rules = pd.read_csv(path, index_col=0, quotechar='"')
    # rules["Column"].replace(" ", "_", inplace=True, regex=True)
    # print(rules)
    return rules.T.to_dict(orient="list")


def meta_wrap(a, b, method):
    print(a, b, method)
    if method == "gt":
        return float(a) > float(b)
    if method == "neq":
        return a != b
    if method == "eq":
        return a == b
    if method == "ge":
        return float(a) >= float(b)
    if method == "le":
        return float(a) <= float(b)
    if method == "lt":
        return float(a) < float(b)


def apply_rules(row, rules, nr=0, decision_path=[]):
    print(nr)
    rule = rules[nr]  # node
    decision_path.append(nr)
    col = rule[0]
    signal = rule[1]
    value = rule[2]
    outcome_y = rule[3]
    outcome_y_type = rule[4]
    outcome_n = rule[5]
    outcome_n_type = rule[6]
    # print(data[col][0])
    if meta_wrap(row[col], value, signal):
        print(outcome_y)
        if outcome_y_type == "final":
            # print("is string")
            return outcome_y
        else:
            return apply_rules(
                row, rules, nr=int(outcome_y), decision_path=decision_path
            )
    else:
        # print(outcome[1])
        if outcome_n_type == "final":
            return outcome_n
        else:
            # print("outcome is nr")
            # print(rules[outcome[1]])
            return apply_rules(row, rules, int(outcome_n), decision_path)


def create_decision(row, rules):
    # print(row)
    decision_path = []
    return apply_rules(row, rules, decision_path=decision_path), decision_path


def save_rules_to_csv(rules, path):
    dd = pd.DataFrame.from_dict(rules, orient="index")
    dd.columns = [
        "Column",
        "evaluator",
        "comparasion",
        "result_ok",
        "result_ok_type",
        "result_nok",
        "result_nok_type",
    ]
    dd.to_csv(path)


def routing(request, rules, rule_nr):

    data = request.json

    if rule_nr in rules.keys():

        decision, decision_path = create_decision(data, rules[rule_nr])
    else:
        return {"message": "Invalid rule number"}, 400
    return jsonify(
        {
            "decision": decision,
            "decision_path": ",".join([str(x) for x in decision_path]),
        }
    )
