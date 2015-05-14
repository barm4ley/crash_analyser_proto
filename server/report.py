


from collections import namedtuple

BASIC_REPORT_ID = 1
FULL_REPORT_ID  = 2

BASIC_REPORT_STR = 'basic_reports'
FULL_REPORT_STR  = 'full_reports'
BUCKETS_STR      = 'buckets'

ReportType = namedtuple('ReportType', 'report_id, report_str')

_knownReportTypes = []
_knownReportTypes.append(ReportType(BASIC_REPORT_ID, BASIC_REPORT_STR))
_knownReportTypes.append(ReportType(FULL_REPORT_ID,  FULL_REPORT_STR))

def convertReportString2ReportId(report_str):
    for (rpt_id, rpt_str) in _knownReportTypes:
        if rpt_str == report_str:
            return rpt_id
    raise ValueError('Unknown report string: {0}'.format(report_str))


def convertReportId2ReportSting(report_id):
    for (rpt_id, rpt_str) in _knownReportTypes:
        if rtp_id == report_id:
            return rpt_str
    raise ValueError('Unknown report id: {0}'.format(report_id))

