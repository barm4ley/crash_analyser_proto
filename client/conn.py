#!/usr/bin/env python

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

def print_data_exchange(url, data_to, data_from):
    return
    pprint('----------------------------------------------------------')
    pprint('URL: ' + url, width = 120)
    pprint('To:')
    pprint(data_to)
    pprint('From:')
    pprint(data_from)

def generate_basic_report():
    return {'label': random.randint(0, 99), 'x': random.random(), 'y': random.random(), 'z': random.random()}

def generate_full_report():
    return {'a': random.random(), 'b': random.random(), 'c': random.random()}

def make_add_report_url(rpt_str):
    return SERVER_URL + rpt_str

def make_add_report_status_url(rpt_str, task_id):
    return make_add_report_url(rpt_str) + '/status/' + task_id

def make_add_report_result_url(rpt_str, task_id):
    return make_add_report_url(rpt_str) + '/result/' + task_id

def send_add_report_request(rpt_str, payload):
    url = make_add_report_url(rpt_str)
    r = requests.post(url, headers = HEADERS, json = payload)
    resp = r.json()

    print_data_exchange(url, payload, resp)

    return resp['task_id']

def send_add_report_status_request(rpt_str, task_id):
    url = make_add_report_status_url(rpt_str, task_id)
    r = requests.get(url)
    resp = r.json()

    print_data_exchange(url, '[GET]', resp)

    return resp

def read_add_report_status_until_ready(rpt_str, task_id):
    while True:
        data = send_add_report_status_request(rpt_str, task_id)
        if data['ready']:
            return data
        else:
            sleep(0.1)

def send_add_report_result_request(rpt_str, task_id):
    url = make_add_report_result_url(rpt_str, task_id)
    r = requests.get(url)
    resp = r.json()

    print_data_exchange(url, '[GET]', resp)

    return resp

def prepare_basic_report(payload):
    meta = {'report_type': 'basic_report'}
    return {'meta': meta, 'data': payload}

def prepare_full_report(basic_report_id, bucket_id, payload):
    meta = {'report_type': 'full_report', 'basic_report_id': basic_report_id, 'bucket_id': bucket_id}
    return {'meta': meta, 'data': payload}

def send_add_full_report_request(basic_report_id, bucket_id, payload):
    meta = {'basic_report_id': basic_report_id, 'bucket_id': bucket_id}
    document = {'meta': meta, 'data': payload}
    r = requests.post(make_add_full_report_url(), headers = HEADERS, json = document)
    return r.json()['task_id']


def upload_report(rpt_str, report):
    task_id = send_add_report_request(rpt_str, report)
    status = read_add_report_status_until_ready(rpt_str, task_id)
    result = send_add_report_result_request(rpt_str, task_id)
    return result


