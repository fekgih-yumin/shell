FROM Python
RUM sudo apt-get install -y git
RUM sudo apt-get install python-pip
RUM pip install django

WORKDIR /opt/
RUN mkdir git
