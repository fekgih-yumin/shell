FROM daocloud.io/python:2-onbuild
WORKDIR picture_app/
CMD [ "python", "python manage.py runserver 0.0.0.0:8001" ]

