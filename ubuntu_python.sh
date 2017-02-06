cd ~
sudo apt-get update
sudo apt-get git
sudo apt-get install python-pip
pip install django
sudo apt-get install mysql-server 
sudo apt-get install mysql-client
pip install mysql-python
pip install oss2
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk 
pip install pillow
cd /
sudo chmod -r 777 /opt/
cd /opt/
mkdir git
cd /git/
git init
git clone git@120.24.217.115:/mnt/opt/git/devopsProjects/ai-photo20161222/python/python-src.git
cd /python-src/picture_app
python manage.py runserver 192.168.199.137:8001  
