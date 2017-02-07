FROM daocloud.io/python:2-onbuild
WORKDIR picture_app/
CMD [ "python", "manage.py runserver 192.168.199.205:8002" ]

