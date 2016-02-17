

FROM debian:latest

RUN apt-get update -qq \
&& apt-get upgrade -y \
&& apt-get install -y python-dev python-pip \
&& apt-get autoremove -y \
&& apt-get clean autoclean

RUN pip install -U pip

ADD en_test.py /en_test/
ADD requirements.txt /en_test/

WORKDIR /en_test

RUN pip install -r requirements.txt 

EXPOSE 8000

CMD gunicorn en_test:app -w 1 -b 0.0.0.0:8000 --log-level info --timeout 120 --pid /en_test/en_test.pid
