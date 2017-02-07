FROM daocloud.io/python:2-onbuild
WORKDIR picture_app/
CMD [ "python", "manage.py runserver 120.76.145.173:8002" ]

