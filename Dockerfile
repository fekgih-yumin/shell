FROM buildpack-deps:jessie
RUN apt-get install -y git
RUN apt-get install python-pip
RUN pip install django

WORKDIR /opt/
RUN mkdir git
