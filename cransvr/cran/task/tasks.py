'''Module defines distibuted tasks that Celery will do on the worker side'''

from celery import Celery, Task, states
from celery.utils.log import get_task_logger
import pymongo
from bson import ObjectId
import random
import itertools
#import report

app = Celery('tasks', broker='amqp://guest@localhost//', backend='amqp')

app.config_from_object('cran.celeryconfig')

logger = get_task_logger(__name__)

#-------------------------------------------------------------------------------

BASIC_REPORT_STR = 'basic_reports'
FULL_REPORT_STR  = 'full_reports'
BUCKETS_STR      = 'buckets'

#-------------------------------------------------------------------------------

class MongoAccessorTask(Task):
    '''Task class provides db caching and simple db operations'''
    abstract = True

    _db = None

    _BUCKETS_COLL_NAME = BUCKETS_STR
    _FULL_REPORTS_COLL_NAME = FULL_REPORT_STR
    _BASIC_REPORTS_COLL_NAME = BASIC_REPORT_STR

    BASIC_REPORT = 1
    FULL_REPORT  = 2

    def report_type_to_collection_name(self, report_type):
        '''Convert report type to the collection it should be stored in'''
        if report_type == self.BASIC_REPORT:
            return self._BASIC_REPORTS_COLL_NAME
        if report_type == self.FULL_REPORT:
            return self._FULL_REPORTS_COLL_NAME
        raise ValueError('Invalid report type')

    @property
    def db(self):
        '''DB access property'''
        if self._db is None:
            db_connection = pymongo.MongoClient(app.conf.DB_URL)
            self._db = db_connection.test
        return self._db

    def add_report(self, report_type, report):
        '''Write report ino DB.
        report_type - type of report to write(basic_reports & full_reports types are supported)
        report - report document to write
        Return: ID of report that has been written
        '''
        coll = self.report_type_to_collection_name(report_type)
        insert_result = self.db[coll].insert_one(report)
        report_id = str(insert_result.inserted_id)
        return report_id

    def get_bucket_id(self, criteria):
        '''Get bucket ID that corresponds to some criteria'''
        bucket_id = None
        find_result = self.db[self._BUCKETS_COLL_NAME].find_one(criteria)
        if find_result:
            bucket_id = find_result['_id']
        else:
            insert_result = self.db[self._BUCKETS_COLL_NAME].insert_one(criteria)
            bucket_id = insert_result.inserted_id
        return str(bucket_id)

    def add_report_to_bucket(self, bucket_id, report_id, report_type):
        '''Connect bucket and report documents in DB'''
        coll = self.report_type_to_collection_name(report_type)
        self.db[self._BUCKETS_COLL_NAME].update_one({'_id': ObjectId(bucket_id)}, {'$addToSet': {coll: ObjectId(report_id)}})

#-------------------------------------------------------------------------------

DEBUG = False

def log_debug(func):
    "This decorator dumps out the arguments passed to a function before calling it"

    if not DEBUG:
        return func

    argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
    fname = func.__name__

    def echo_func(*args,**kwargs):
        logger.info("{0}:{1}".format(fname, ', '.join(
            '%s=%r' % entry
            for entry in itertools.chain(itertools.izip(argnames,args), kwargs.items()))))
        return func(*args, **kwargs)

    return echo_func


def get_task_info(async_result):
    '''Extract information about AsyncResult'''
    res = {}
    res['id']    = async_result.id
    res['state'] = async_result.state
    res['ready'] = (res['state'] in states.READY_STATES)
    res['success'] = async_result.successful()
    return res


@app.task(name="basic.report.add", bind=True, base=MongoAccessorTask)
def add_report_task(self, report):
    '''Write basic report to the DB'''

    data = report['data']
    meta = report['meta']

    report_type = self.BASIC_REPORT

    try:
        # Insert report into DB
        report_id = self.add_report(report_type, data)

        # Get bucket id for the label
        bucket_id = self.get_bucket_id({'label': data['label']})

        # Update bucket
        self.add_report_to_bucket(bucket_id, report_id, report_type)
    except pymongo.errors.AutoReconnect as exc:
        logger.warning('AutoReconnect exception caught: {0}'.format(exc))
        self.retry(exc = exc)

    return {'report_id': report_id, 'bucket_id': bucket_id, 'full_report_needed': random.choice([True, False])}

@app.task(name="full.report.add", bind=True, base=MongoAccessorTask)
def add_full_report_task(self, report):
    '''Write full report to the DB'''

    data = report['data']
    meta = report['meta']

    # Convert document(append basic object id to the full report document)
    data['basic_report_id'] = meta['basic_report_id']

    report_type = self.FULL_REPORT

    try:
        # Insert report into DB
        report_id = self.add_report(report_type, data)

        # Update bucket
        bucket_id = meta['bucket_id']
        self.add_report_to_bucket(bucket_id, report_id, report_type)
    except pymongo.errors.AutoReconnect as exc:
        logger.warning('AutoReconnect exception caught: {0}'.format(exc))
        self.retry(exc = exc)

    return {'report_id': report_id, 'bucket_id': bucket_id}

@app.task(name='test.task', bind=True)
def test_task(self):
    logger.info("10 secs passed...")
