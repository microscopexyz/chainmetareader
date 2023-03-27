FROM python:3.9

WORKDIR /app
ADD alembic.ini alembic.ini
ADD dbmigration/ dbmigration/
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["alembic", "upgrade", "head"]
