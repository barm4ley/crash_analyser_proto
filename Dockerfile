FROM python:3.4-slim

MAINTAINER Max Musich <maxim@unity3d.com>

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

ADD . /home/user
WORKDIR /home/user

RUN pip3.4 install --upgrade pip
RUN pip3.4 install -r ./requirements.txt

EXPOSE 5555

USER user

CMD ["celery", "worker"]
