

FROM debian:latest
MAINTAINER Regner Blok-Andersen <shadowdf@gmail.com>

ENV NOTIFICATION_TOPIC "send_notification"

ADD en_test.py /en_test/
ADD requirements.txt /en_test/

WORKDIR /en_test

RUN apt-get update -qq \
&& apt-get upgrade -y -qq \
&& apt-get install -y -qq python-dev python-pip \
&& apt-get autoremove -y \
&& apt-get clean autoclean \
&& pip install -qU pip \
&& pip install -r requirements.txt

EXPOSE 8000

CMD gunicorn en_test:app -w 1 -b 0.0.0.0:8000 --log-level info --timeout 120 --pid /en_test/en_test.pid
