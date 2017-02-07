FROM buildpack-deps:jessie
RUN sudo apt-get install -y git
RUN sudo apt-get install python-pip
RUN pip install django

WORKDIR /opt/
RUN mkdir git
