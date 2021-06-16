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

RUN black src --check --diff

EXPOSE 8000

COPY --from=node /app/src/barbook_app/static /app/src/barbook_app/static

RUN python src/manage.py collectstatic --noinput

CMD python -m spacy download en && python src/manage.py makemigrations && python src/manage.py migrate && gunicorn barbook_project.wsgi --chdir src --bind 0.0.0.0 --preload --log-file -
