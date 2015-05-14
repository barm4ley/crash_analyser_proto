
SECRET_KEY = "top_secret"

CELERY_RESULT_BACKEND = "mongodb://172.19.8.101:27017/"
#CELERY_RESULT_BACKEND = 'amqp'
CELERY_MONGODB_BACKEND_SETTINGS = {
        'database': 'celerydb',
        'taskmeta_collection': 'taskmeta_collection',
}

BROKER_URL = "amqp://guest:guest@172.19.8.101:5672//"
CELERY_IMPORTS = ("tasks",)

#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'msgpack'
#CELERY_ACCEPT_CONTENT=['json', 'msgpack']

CELERY_ACCEPT_CONTENT=['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = CELERY_TASK_SERIALIZER

CELERY_DISABLE_RATE_LIMITS = True

DB_URL = "mongodb://172.19.8.101:27017"
