#!/usr/bin/env python

'''Flask-based web server to process CrashAnalyser reports'''

import json
from flask import Flask, jsonify, request
from ..task.tasks import add_report_task, add_full_report_task, get_task_info, BASIC_REPORT_STR, FULL_REPORT_STR

app = Flask(__name__)

task_selector = {BASIC_REPORT_STR: add_report_task, FULL_REPORT_STR: add_full_report_task}


@app.route("/<report_type>", methods = ['POST'])
def add_report(report_type):
    '''Route to process report adding.
    report_type - type of report to post(basic_reports & full_reports types are supported)
    Returns: JSON document with Celery task id
    '''
    data = request.get_json()
    task = task_selector[report_type].apply_async([data])
    return jsonify({'task_id':task.id})


@app.route("/<report_type>/status/<task_id>")
def get_add_report_status(report_type, task_id):
    '''Route to get "report add" status.
    report_type - type of report to post(basic_reports & full_reports types are supported)
    task_id - identifier of Celery task.
    Returns: JSON document with Celery task status
    '''
    task = task_selector[report_type].AsyncResult(task_id)
    resp = get_task_info(task)
    return jsonify(resp)


@app.route("/<report_type>/result/<task_id>")
def get_add_report_result(report_type, task_id):
    '''Route to get "report add" restult.
    report_type - type of report to post(basic_reports & full_reports types are supported)
    task_id - identifier of Celery task.
    Returns: JSON document with Celery task execution result
    '''
    task = task_selector[report_type].AsyncResult(task_id)
    if task.ready():
        return jsonify(task.get())
    else:
        return '',  404



def start_operation(**kwargs):
    app.run(**kwargs)

if __name__ == "__main__":
    start_operation(host="0.0.0.0", port=5000, debug=True)
