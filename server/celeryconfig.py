
#--- RESULT BACKEND SETTINGS ---#

# RabbitMQ
#CELERY_RESULT_BACKEND = 'amqp'

# Redis
CELERY_RESULT_BACKEND = 'redis://172.19.8.101:6379/0'

# MongoDB
#CELERY_RESULT_BACKEND = "mongodb://172.19.8.101:27017/"
#CELERY_MONGODB_BACKEND_SETTINGS = {
        #'database': 'celerydb',
        #'taskmeta_collection': 'taskmeta_collection',
#}


#--- MESSAGE BROKER SETTINGS ---#
BROKER_URL = "amqp://guest:guest@172.19.8.101:5672//"


#--- MODULES TO USE ---#
CELERY_IMPORTS = ("tasks",)


#--- EXCHANGE DATA FORMAT ---#

#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'msgpack'
#CELERY_ACCEPT_CONTENT=['json', 'msgpack']

CELERY_ACCEPT_CONTENT=['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = CELERY_TASK_SERIALIZER

#--- OTHER OPTIONS ---#
CELERY_DISABLE_RATE_LIMITS = True

#---------------------------------------------------------------#
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'do-each-10-sec': {
        'task': 'test.task',
        'schedule': timedelta(seconds=10)
    },
}

CELERY_TIMEZONE = 'UTC'
#---------------------------------------------------------------#


DB_URL = "mongodb://172.19.8.101:27017"
