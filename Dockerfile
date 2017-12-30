FROM python:3.6-alpine

# Add curl for automatic reporting
RUN apk add --update curl && \
    rm -rf /var/cache/apk/*

# install requirements
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy files to the container
RUN mkdir /dashboard/
COPY . /dashboard/
WORKDIR /dashboard/
EXPOSE 8000

# Sets production config mode
ENV FLASK_CONFIG="production"

# Create the empty database
RUN python manage.py setup

# Startup the cron service and gunicorn
gunicorn -c gunicorn_conf.py manage:app