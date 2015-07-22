'''Module with CrashAnalyser client helper functions.'''

import requests
import json
import random
from time import sleep
from pprint import pprint

SERVER_URL = 'http://localhost:5000/'
HEADERS = {'Content-type': 'application/json', 'Accept': '*/*'}

BASIC_REPORT_STR = 'basic_reports'
FULL_REPORT_STR = 'full_reports'
BUCKETS_STR = 'buckets'

DEBUG_ENABLED = True

def print_data_exchange(url, data_to, data_from):
    if not DEBUG_ENABLED:
        return
    pprint('----------------------------------------------------------')
    pprint('URL: ' + url, width = 120)
    pprint('To:')
    pprint(data_to)
    pprint('From:')
    pprint(data_from)

def generate_basic_report():
    '''Generate JSON with basic report data (simulation).'''
    return {'label': random.randint(0, 99), 'x': random.random(), 'y': random.random(), 'z': random.random()}

def generate_full_report():
    '''Generate JSON with full report data (simulation).'''
    return {'a': random.random(), 'b': random.random(), 'c': random.random()}

def make_add_report_url(rpt_str):
    '''Produce a string with URL client can use to add report.
    rpt_str - report type (can be 'basic_reports' or 'full_reports').
    '''
    return SERVER_URL + rpt_str

def make_add_report_status_url(rpt_str, task_id):
    '''Produce a string with URL client can use to get status of add report procedure.
    rpt_str - report type (can be 'basic_reports' or 'full_reports').
    task_id - identifier of Celery task.
    '''
    return make_add_report_url(rpt_str) + '/status/' + task_id

def make_add_report_result_url(rpt_str, task_id):
    '''Produce a string with URL client can use to get result of add report procedure.
    rpt_str - report type (can be 'basic_reports' or 'full_reports').
    task_id - identifier of Celery task.
    '''
    return make_add_report_url(rpt_str) + '/result/' + task_id


def send_add_report_request(rpt_str, report):
    '''Send HTTP "add report" request to server.
    rpt_str - report type (can be 'basic_reports' or 'full_reports').
    payload - report to send(dict).
    Returns: Celery task identifier.
    '''
    url = make_add_report_url(rpt_str)
    r = requests.post(url, headers = HEADERS, json = report)
    resp = r.json()

    print_data_exchange(url, report, resp)

    return resp['task_id']


def send_add_report_status_request(rpt_str, task_id):
    '''Send HTTP "add report" status request to server.
    rpt_str - report type (can be 'basic_reports' or 'full_reports').
    task_id - identifier of Celery task.
    Returns: Information about Celery task(JSON document).
    '''
    url = make_add_report_status_url(rpt_str, task_id)
    r = requests.get(url)
    resp = r.json()

    print_data_exchange(url, '[GET]', resp)

    return resp

def read_add_report_status_until_ready(rpt_str, task_id):
    '''Fetch "add report" status until become ready.
    rpt_str - report type (can be 'basic_reports' or 'full_reports').
    task_id - identifier of Celery task.
    '''
    while True:
        data = send_add_report_status_request(rpt_str, task_id)
        if data['ready']:
            return data
        else:
            sleep(0.1)

def send_add_report_result_request(rpt_str, task_id):
    '''Send HTTP "add report" result request to server.
    rpt_str - report type (can be 'basic_reports' or 'full_reports').
    task_id - identifier of Celery task.
    Returns: Task execution results.
    '''
    url = make_add_report_result_url(rpt_str, task_id)
    r = requests.get(url)
    resp = r.json()

    print_data_exchange(url, '[GET]', resp)

    return resp

def prepare_basic_report(payload):
    '''Convert basic report into format understandable for server.'''
    meta = {'report_type': 'basic_report'}
    return {'meta': meta, 'data': payload}

def prepare_full_report(basic_report_id, bucket_id, payload):
    '''Convert basic report into format understandable for server.
    basic_report_id - id of basic report this full report should be connected to.
    bucket_id - id of bucket this full report should be added to.
    '''
    meta = {'report_type': 'full_report', 'basic_report_id': basic_report_id, 'bucket_id': bucket_id}
    return {'meta': meta, 'data': payload}


def upload_report(rpt_str, report):
    '''Do whole cycle of report uploading: post report, wait for results to become ready, read them and return.
    rpt_str - report type (can be 'basic_reports' or 'full_reports').
    task_id - identifier of Celery task.
    '''
    task_id = send_add_report_request(rpt_str, report)
    status = read_add_report_status_until_ready(rpt_str, task_id)
    result = send_add_report_result_request(rpt_str, task_id)
    return result


