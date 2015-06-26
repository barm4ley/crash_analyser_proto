from os import getenv
from datetime import timedelta

#--- RESULT BACKEND SETTINGS ---#

# Redis
RESULT_BACKEND_ADDR = getenv('RESULT_BACKEND_ADDR', 'localhost')
RESULT_BACKEND_PORT = getenv('RESULT_BACKEND_PORT', 6379)
CELERY_RESULT_BACKEND = 'redis://{url}:{port}/0'.format(url=RESULT_BACKEND_ADDR, port=RESULT_BACKEND_PORT)

#--- MESSAGE BROKER SETTINGS ---#
#BROKER_URL = "amqp://guest:guest@10.0.2.15:5672//"
MESSAGE_BROKER_ADDR = getenv('MESSAGE_BROKER_ADDR', 'localhost')
MESSAGE_BROKER_PORT = getenv('MESSAGE_BROKER_PORT', 5672)
MESSAGE_BROKER_USER = getenv('MESSAGE_BROKER_USER', 'admin')
MESSAGE_BROKER_PASS = getenv('MESSAGE_BROKER_PASS', 'admin')
BROKER_URL = "amqp://{user}:{password}@{url}:{port}//".format(
        user=MESSAGE_BROKER_USER,
        password=MESSAGE_BROKER_PASS,
        url=MESSAGE_BROKER_ADDR,
        port=MESSAGE_BROKER_PORT)

#--- MODULES TO USE ---#
CELERY_IMPORTS = ("tasks",)


#--- EXCHANGE DATA FORMAT ---#

CELERY_ACCEPT_CONTENT=['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = CELERY_TASK_SERIALIZER

#--- OTHER OPTIONS ---#
CELERY_DISABLE_RATE_LIMITS = True

#---------------------------------------------------------------#

CELERYBEAT_SCHEDULE = {
    'do-each-10-sec': {
        'task': 'test.task',
        'schedule': timedelta(seconds=10)
    },
}

CELERY_TIMEZONE = 'UTC'
#---------------------------------------------------------------#


STORAGE_ADDR = getenv('STORAGE_ADDR', 'localhost')
STORAGE_PORT = getenv('STORAGE_PORT', 27017)
DB_URL = "mongodb://{url}:{port}".format(url=STORAGE_ADDR, port=STORAGE_PORT)


print("CELERY_RESULT_BACKEND: {}".format(CELERY_RESULT_BACKEND))
print("BROKER_URL: {}".format(BROKER_URL))
print("DB_URL: {}".format(DB_URL))
