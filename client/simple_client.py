#!/usr/bin/env python

import conn
from pprint import pprint

def main():

    pprint('==========================================================')
    pprint('==========================================================')
    conn.DEBUG_ENABLED = True
    basic_report = conn.prepare_basic_report(conn.generate_basic_report())
    result = conn.upload_report(conn.BASIC_REPORT_STR, basic_report)
    if result['full_report_needed']:
        full_report = conn.prepare_full_report(result['report_id'], result['bucket_id'], conn.generate_full_report())
        result = conn.upload_report(conn.FULL_REPORT_STR, full_report)

if __name__ == "__main__":
    main()
