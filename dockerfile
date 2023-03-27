# base image
FROM python:3.9 AS base
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# dbmigration image
FROM base as db_migration
WORKDIR /app
ADD alembic.ini alembic.ini
ADD dbmigration/ dbmigration/
CMD ["alembic", "upgrade", "head"]

# development image
FROM base as development
WORKDIR /app
ADD . .
CMD ["bash", "-c", "trap : TERM INT; sleep infinity & wait"]
