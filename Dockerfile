FROM python:3.4-slim

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user

ENV CELERY_VERSION 3.1.18

RUN pip install celery=="$CELERY_VERSION"
#RUN pip install pymongo
RUN pip install https://github.com/mongodb/mongo-python-driver/archive/3.0rc1.tar.gz
RUN pip install -U celery[redis]
RUN pip install flower

RUN { \
	echo 'import os'; \
	echo "BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://')"; \
} > celeryconfig.py

# --link some-rabbit:rabbit "just works"
#ENV CELERY_BROKER_URL amqp://guest@rabbit

EXPOSE 5555

USER user
CMD ["celery", "worker"]
