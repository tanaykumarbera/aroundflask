FROM ubuntu:14.04
MAINTAINER Sudipta Sen <sanborn.sen@gmail.com>
RUN apt-get update
RUN apt-get install -y python-pip python-dev libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk libmysqlclient-dev
RUN mkdir aroundapp
RUN cd aroundapp
COPY . /aroundapp/
RUN pip install -r /aroundapp/extra/requirements.txt
