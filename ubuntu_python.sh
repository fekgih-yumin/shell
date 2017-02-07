FROM ubuntu16-python2.7
RUM sudo apt-get install -y git
RUM sudo apt-get install python-pip
RUM pip install django

WORKDIR /opt/
RUN mkdir git
WORKDIR /opt/git/
RUN git init
RUN git clone git@120.24.217.115:/mnt/opt/git/devopsProjects/ai-photo20161222/python/python-src.git

