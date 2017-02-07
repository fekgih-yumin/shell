FROM buildpack-deps:jessie
#RUN apt-get install -y git
#RUN apt-get install python-pip
#RUN pip install django

WORKDIR /opt/
RUN mkdir git
WORKDIR git/
RUN git init
RUN git clone git@120.24.217.115:/mnt/opt/git/devopsProjects/ai-photo20161222/python/python-src.git

