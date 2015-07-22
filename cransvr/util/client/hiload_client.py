#!/usr/bin/env python

import conn
import threading

def thread_func():
    while True:
        basic_report = conn.prepare_basic_report(conn.generate_basic_report())
        result = conn.upload_report(conn.BASIC_REPORT_STR, basic_report)
        result = conn.upload_report(conn.BASIC_REPORT_STR, basic_report)
        if result['full_report_needed']:
            full_report = conn.prepare_full_report(result['report_id'], result['bucket_id'], conn.generate_full_report())
            result = conn.upload_report(conn.FULL_REPORT_STR, full_report)

def main():
    conn.DEBUG_ENABLED = False

    threads = []
    for i in range(10):
        t = threading.Thread(target = thread_func)
        threads.append(t)
        t.start()

if __name__ == "__main__":
    main()
