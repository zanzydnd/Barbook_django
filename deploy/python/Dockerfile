FROM node:14-alpine as node
WORKDIR /app/src/barbook_app/static/
COPY src/barbook_app/static/package-lock.json .
COPY src/barbook_app/static/package.json .
RUN npm ci

COPY src/barbook_app/static/ .

FROM python:3.8
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

COPY  img_source/ /app/
RUN ls -la /app/img_source/

COPY --from=node /app/src/barbook_app/static /app/src/barbook_app/static

RUN python src/manage.py collectstatic --noinput

CMD python3 -m spacy download en && python3 src/manage.py makemigrations && python3 src/manage.py migrate && python3 src/manage.py initadmin && gunicorn barbook_project.wsgi --chdir src --bind 0.0.0.0 --preload --log-file -
