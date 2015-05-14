#!/usr/bin/env python

import json
from flask import Flask, jsonify, request
from tasks import add_report_task, add_full_report_task, get_task_info
import report

app = Flask(__name__)

task_selector = {report.BASIC_REPORT_ID: add_report_task, report.FULL_REPORT_ID: add_full_report_task}


@app.route("/<report_type>", methods = ['POST'])
def add_report(report_type):
    report_id = report.convertReportString2ReportId(report_type)
    data = request.get_json()
    task = task_selector[report_id].apply_async([data])
    return jsonify({'task_id':task.id})


@app.route("/<report_type>/status/<task_id>")
def get_add_report_status(report_type, task_id):
    report_id = report.convertReportString2ReportId(report_type)
    task = task_selector[report_id].AsyncResult(task_id)
    resp = get_task_info(task)
    return jsonify(resp)


@app.route("/<report_type>/result/<task_id>")
def get_add_report_result(report_type, task_id):
    report_id = report.convertReportString2ReportId(report_type)
    task = task_selector[report_id].AsyncResult(task_id)
    if task.ready():
        return jsonify(task.get())
    else:
        return '',  404

#################################################################

@app.route("/<first>/<second>/")
def test_route(first, second):
    resp = {'first':first,'second':second}
    #return jsonify(resp), 404
    return '', 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
