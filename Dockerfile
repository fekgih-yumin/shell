FROM daocloud.io/python:2-onbuild
WORKDIR picture_app/
CMD [ "python", "manage.py runserver server.5fech.com:8002" ]

